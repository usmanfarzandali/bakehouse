odoo.define('vpcs_pos_kitchen.DB', function(require) {
    "use strict";

    var PosDB = require('point_of_sale.DB');
    var rpc = require('web.rpc');

    PosDB.include({
        remove_order: function(order_id, sync_order = false) {
            this._super.apply(this, arguments);
            if (sync_order) return true;
            this.pos_synch_remove([order_id]);
        },
        reload_orders: function() {
            var self = this;
            return new Promise(function(resolve, reject) {
                rpc.query({
                    model: 'pos.order.synch',
                    method: 'synch_all',
                    args: [],
                }).then(function(result) {
                    self.synch_orders = result;
                    resolve();
                }).catch(function() {
                    reject();
                });
            });
        },
        pos_synch_update: function(action, orders) {
            var self = this;
            var uid = orders[0].uid;
            if (action == 'add') {
                orders = _.filter(orders, function(order) {
                    return order && order.lines.length;
                })
            }
            if (!orders.length) {
                action = 'remove_line';
                orders = [{
                    'uid': uid,
                    'lines': []
                }];
            }
            var json_orders = JSON.stringify(orders);
            return new Promise(function(resolve, reject) {
                rpc.query({
                    model: 'pos.order.synch',
                    method: 'update_orders',
                    args: [action, json_orders],
                }).then(function(result) {
                    resolve();
                }).catch(function() {
                    reject();
                });
            });
        },
        pos_synch_remove: function(order_uids) {
            if (!order_uids.length) {
                return;
            }
            return new Promise(function(resolve, reject) {
                rpc.query({
                    model: 'pos.order.synch',
                    method: 'remove_order',
                    args: [order_uids],
                }).then(function(result) {
                    resolve();
                }).catch(function() {
                    console.error('Failed to remove orders : ', order_uids);
                    reject();
                });
            });
        },
        pos_synch_all_parsed: function(orders) {
            var self = this;
            orders = _.filter(orders, function(_order) {
                return _order.order_data;
            });

            var parsed_orders = [];
            _.each(orders, function(order) {
                var parsed_row = $.parseJSON(order.order_data);
                var already_added = _.where(parsed_orders, {
                    'uid': parsed_row.uid
                });
                if (already_added.length) {
                    return;
                }
                var orderlines = [];
                var prod_ids = _.keys(self.product_by_id);
                _.each(parsed_row.lines, function(oline) {
                    if (oline.state == "done") return;
                    var prod_id = oline.product_id;
                    if (prod_id && _.indexOf(prod_ids, prod_id.toString()) > -1) {
                        oline.product = self.product_by_id[prod_id];
                        orderlines.push(oline);
                    }
                });
                if (!orderlines.length) {
                    return;
                }
                if (parsed_row.partner_id) {
                    parsed_row.partner = self.partner_by_id[parsed_row.partner_id];
                }
                parsed_row.orderlines = _.sortBy(orderlines, "id");
                parsed_orders.push(parsed_row);
            });
            return parsed_orders;
        },
        pos_orderline_state: function(uid, line_id, state) {
            var self = this;
            var def = new $.Deferred();
            if (!uid || !line_id || !state) {
                return def.reject();
            }
            return new Promise(function(resolve, reject) {
                rpc.query({
                    model: 'pos.order.synch',
                    method: 'orderline_state',
                    args: [uid, line_id, state],
                }).then(function(result) {
                    resolve();
                }).catch(function() {
                    console.error('Failed to POS Synch Orderline State : ', uid, state);
                    reject();
                });
            });
        }
    });
});