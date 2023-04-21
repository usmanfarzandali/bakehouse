odoo.define('vpcs_pos_kitchen.models', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var session = require('web.session');
    require('pos_restaurant.multiprint');


    models.PosModel.prototype.models.push({
        model: 'pos.order.synch',
        fields: ['order_uid', 'order_data', 'write_date', 'pos_id'],
        loaded: function(self, synch_orders) {
            self.db.synch_orders = synch_orders;
        },
    });

    const PosCategory = _.find(models.PosModel.prototype.models, function(p) {
        if (p.model == 'pos.category') {
            return true;
        }
        return false;
    });

    PosCategory.fields.push('color');

    var PosProduct = _.find(models.PosModel.prototype.models, function(p) {
        if (p.model == 'product.product') {
            return true;
        }
        return false;
    });
    var _super_loaded = PosProduct.loaded;

    PosProduct.loaded = function(self, products) {
        var categories = self.db.category_by_id;
        _.each(products, function(prod) {
            prod.bgcolor = 'white';
            if (prod.pos_categ_id.length) {
                var categ = categories[prod.pos_categ_id[0]];
                if (categ) {
                    prod.bgcolor = categ.color;
                }
            }
        });
        _super_loaded(self, products);
    };

    var _super_posmodel = models.PosModel;
    models.PosModel = models.PosModel.extend({
        initialize: function(attributes, options) {
            var self = this;
            _super_posmodel.prototype.initialize.apply(this, arguments);
            this.priority_by_key = _.extend({}, {
                'low': 'Low',
                'normal': 'Normal',
                'high': 'High',
            });
        },
        delete_current_order: function() {
            var order = this.get_order();
            this.db.pos_synch_remove([order.uid]);
            _super_posmodel.prototype.delete_current_order.apply(this, arguments);
        },
        set_order_status: function(new_order, Order) {
            var self = this;
            new_order.set_priority(Order.priority);
            new_order.set_old_priority(Order.old_priority);
            this.trigger('change', new_order);
        },
        // sync_to_server: function(table) {
        //     var self = this;
        //     var ids_to_remove = this.db.get_ids_to_remove_from_server();

        //     this.set_synch('connecting', 1);
        //     this._get_from_server(table.id).then(function(server_orders) {
        //         var orders = self.get_order_list();
        //         server_orders.forEach(function(server_order) {
        //             if (server_order.lines.length) {
        //                 var new_order = new models.Order({}, {
        //                     pos: self,
        //                     json: server_order
        //                 });
        //                 self.get("orders").add(new_order);
        //                 self.set_order_status(new_order, server_order);
        //                 self.set_order_line_status(new_order, server_order);
        //                 new_order.save_to_db();
        //             }
        //         })
        //         orders.forEach(function(order) {
        //             if (order.server_id) {
        //                 self.get("orders").remove(order);
        //                 order.destroy();
        //             }
        //         });
        //         if (!ids_to_remove.length) {
        //             self.set_synch('connected');
        //         } else {
        //             self.remove_from_server_and_set_sync_state(ids_to_remove);
        //         }
        //     }).catch(function(reason) {
        //         self.set_synch('error');
        //     }).finally(function() {
        //         self.set_order_on_table();
        //     });
        // },
        _save_to_server: function(orders, options) {
            if (!orders || !orders.length) {
                return Promise.resolve([]);
            }

            options = options || {};

            var self = this;
            var timeout = typeof options.timeout === 'number' ? options.timeout : 30000 * orders.length;

            // Keep the order ids that are about to be sent to the
            // backend. In between create_from_ui and the success callback
            // new orders may have been added to it.
            var order_ids_to_sync = _.pluck(orders, 'id');

            // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
            // then we want to notify the user that we are waiting on something )
            var args = [_.map(orders, function(order) {
                order.to_invoice = options.to_invoice || false;
                return order;
            })];
            args.push(options.draft || false);
            return this.rpc({
                    model: 'pos.order',
                    method: 'create_from_ui',
                    args: args,
                    kwargs: {
                        context: this.session.user_context
                    },
                }, {
                    timeout: timeout,
                    shadow: !options.to_invoice
                })
                .then(function(server_ids) {
                    _.each(order_ids_to_sync, function(order_id) {
                        self.db.remove_order(order_id, true);
                    });
                    self.set('failed', false);
                    return server_ids;
                }).catch(function(reason) {
                    var error = reason.message;
                    console.warn('Failed to send orders:', orders);
                    if (error.code === 200) { // Business Logic Error, not a connection problem
                        // Hide error if already shown before ...
                        if ((!self.get('failed') || options.show_error) && !options.to_invoice) {
                            self.set('failed', error);
                            throw error;
                        }
                    }
                    throw error;
                });
        },
        // set_order_line_status: function(new_order, Order) {
        //     var self = this;
        //     new_order.get_orderlines().forEach(function(line) {
        //         Order.lines.forEach(function(ll) {
        //             if (line.id == ll[2].cid) {
        //                 line.set_state(ll[2]['state'])
        //                 line.set_qty_change(ll[2]['has_qty_change']);
        //                 self.trigger('change', line);
        //             }
        //         });
        //     });
        // },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attributes, options) {
            _super_order.initialize.apply(this, arguments);
            this.priority = this.priority || 'normal';
            this.old_priority = this.old_priority || 'normal';
            this.sync_order_flag = false;
            this.priority_display = this.pos.priority_by_key[this.priority];
            this.order_to_kitchen = false;
        },
        set_sync_order_flag: function(sync_order_flag) {
            this.sync_order_flag = sync_order_flag;
            this.trigger('change');
        },
        get_sync_order_flag: function() {
            return this.sync_order_flag;
        },
        set_old_priority: function(priority) {
            this.old_priority = this.priority;
            this.trigger('change');
        },
        set_priority: function(priority) {
            this.old_priority = this.priority;
            this.priority = priority;
            this.trigger('change', this);
            this.send_to_kitchen();
        },
        get_old_priority: function() {
            return this.old_priority;
        },
        get_priority: function() {
            return this.priority;
        },
        send_to_kitchen: async function() {
            if (!this.orderlines.length) {
                return;
            }
            await this.update_to_kitchen();
        },
        update_to_kitchen: async function() {
            var action = "add";
            if (this.order_to_kitchen) {
                action = "update";
            }
            var line_models = [];
            for (var i = 0; i < this.orderlines.models.length; i++) {
                var order_line = this.orderlines.models[i];
                if (order_line.printable() && !order_line.order_to_kitchen) {
                    if (!order_line.get_state()) {
                        order_line.set_state('new');
                    }
                    line_models.push(order_line.export_as_JSON());
                };
            }
            var order = this.export_as_JSON();
            order.lines = line_models;
            await this.pos.db.pos_synch_update(action, [order]);
        },
        export_as_JSON: function() {
            var data = _super_order.export_as_JSON.apply(this, arguments);
            data.old_priority = this.old_priority;
            data.priority = this.priority;
            data.sync_order_flag = this.sync_order_flag;
            return data;
        },
        init_from_JSON: function(json) {
            this.priority = json.priority;
            this.old_priority = json.old_priority;
            this.sync_order_flag = json.sync_order_flag;
            _super_order.init_from_JSON.call(this, json);
        },
        capital_first_letter: function(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        },
        saveChanges: function() {
            this.old_priority = this.get_priority();
            _super_order.saveChanges.call(this, arguments);
        },
        export_for_printing: function() {
            var r = _super_order.export_for_printing.call(this);
            return _.extend(r, {
                'priority': this.get_priority(),
                'old_priority': this.get_old_priority(),
                'priority_display': this.priority_display,
            });
        },
        // build_line_resume: function() {
        //     var resume = {};
        //     this.orderlines.each(function(line) {
        //         if (line.mp_skip) {
        //             return;
        //         }
        //         var line_hash = line.get_line_diff_hash();
        //         var qty = Number(line.get_quantity());
        //         var note = line.get_note();
        //         var product_id = line.get_product().id;
        //         var state = line.get_state();
        //         var has_qty_change = line.get_has_qty_change();
        //         if (typeof resume[line_hash] === 'undefined') {
        //             resume[line_hash] = {
        //                 qty: qty,
        //                 note: note,
        //                 product_id: product_id,
        //                 product_name_wrapped: line.generate_wrapped_product_name(),
        //                 state: state,
        //                 has_qty_change: has_qty_change,
        //             };
        //         } else {
        //             resume[line_hash].qty += qty;
        //         }

        //     });
        //     return resume;
        // },
        // computeChanges: function(categories) {
        //     var current_res = this.build_line_resume();
        //     var old_res = this.saved_resume || {};
        //     var line_hash;
        //     var res = _super_order.computeChanges.call(this);
        //     var old_priority = this.old_priority || 'normal';
        //     var current_priority = this.get_priority();

        //     for (line_hash in current_res) {
        //         var curr = current_res[line_hash];
        //         var old = {};
        //         var found = false;
        //         for (var id in old_res) {
        //             if (old_res[id].product_id === curr.product_id) {
        //                 old = old_res[id];
        //             }
        //             if (old_res[id].product_id === curr.product_id && !curr.state) {
        //                 found = true;
        //                 break;
        //             }
        //         }
        //         if (found) {
        //             res.new.push({
        //                 'id': curr.product_id,
        //                 'name': this.pos.db.get_product_by_id(curr.product_id).display_name,
        //                 'name_wrapped': curr.product_name_wrapped,
        //                 'note': curr.note,
        //                 'qty': curr.qty,
        //             });
        //         } else if (old.product_id === curr.product_id && old.qty === curr.qty && !curr.has_qty_change) {
        //             res.new = [];
        //         } else if (!found) {
        //             res.new.push({
        //                 'id': curr.product_id,
        //                 'name': this.pos.db.get_product_by_id(curr.product_id).display_name,
        //                 'name_wrapped': curr.product_name_wrapped,
        //                 'note': curr.note,
        //                 'qty': curr.qty,
        //             });
        //         } else if (old.qty < curr.qty && curr.has_qty_change) {
        //             res.new.push({
        //                 'id': curr.product_id,
        //                 'name': this.pos.db.get_product_by_id(curr.product_id).display_name,
        //                 'name_wrapped': curr.product_name_wrapped,
        //                 'note': curr.note,
        //                 'qty': curr.qty - old.qty,
        //             });
        //         } else if (old.qty > curr.qty) {
        //             res.cancelled.push({
        //                 'id': curr.product_id,
        //                 'name': this.pos.db.get_product_by_id(curr.product_id).display_name,
        //                 'name_wrapped': curr.product_name_wrapped,
        //                 'note': curr.note,
        //                 'qty': old.qty - curr.qty,
        //             });
        //         }
        //     }

        //     if (old_priority !== current_priority) {
        //         if (current_priority) {
        //             res.new.push({
        //                 name: "Order Priority",
        //                 priority: this.capital_first_letter(this.get_priority()),
        //                 product_name_wrapped: ["Order Priority"],
        //                 name_wrapped: ["Order Priority"],
        //                 order: this.uid,
        //                 'qty': 0,
        //                 note: '',
        //             });
        //         }
        //         if (old_priority) {
        //             res.cancelled.push({
        //                 name: "Order Priority",
        //                 'product_name_wrapped': ["Order Priority"],
        //                 name_wrapped: ["Order Priority"],
        //                 priority: this.capital_first_letter(this.get_old_priority()),
        //                 order: this.uid,
        //                 'qty': 0,
        //                 note: '',
        //             });
        //             res.old_priority = this.capital_first_letter(old_priority);
        //         }
        //     }
        //     res.priority = this.capital_first_letter(current_priority);
        //     return res;
        // },
    });

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.call(this, attr, options);
            this.state = this.state || "";
            this.has_qty_change = false;
        },
        set_note: function(note) {
            _super_orderline.set_note.apply(this, arguments);
            this.order.send_to_kitchen();
        },
        set_state: function(state) {
            this.state = state;
            this.trigger('change', this);
        },
        get_state: function(state) {
            return this.state;
        },
        set_qty_change: function(flag) {
            this.has_qty_change = flag
            this.trigger('change', this);
        },
        get_has_qty_change: function() {
            return this.has_qty_change;
        },
        can_be_merged_with: function(orderline) {
            var res = _super_orderline.can_be_merged_with.call(this, orderline);
            if (orderline && orderline.get_state() !== this.get_state()) {
                res = false;
            }
            return res;
        },
        clone: function() {
            var orderline = _super_orderline.clone.call(this);
            orderline.state = this.state;
            return orderline;
        },
        export_as_JSON: function() {
            var json = _super_orderline.export_as_JSON.apply(this, arguments);
            json.state = this.state;
            json.has_qty_change = this.has_qty_change;
            json.cid = this.id;
            return json;
        },
        init_from_JSON: function(json) {
            _super_orderline.init_from_JSON.apply(this, arguments);
            this.state = json.state;
            this.has_qty_change = json.has_qty_change;
            this.id = parseInt(json.cid) ? parseInt(json.cid) : this.id;
        },
    });

});