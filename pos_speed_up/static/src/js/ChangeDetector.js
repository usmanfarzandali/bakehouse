/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
*/
odoo.define('pos_speed_up.ChangeDetector', function (require) {
    "use strict";
    var rpc = require('web.rpc');
    var indexedDB = require('pos_speed_up.indexedDB');
    var models = require('point_of_sale.models');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { useState } = owl;

    if (!indexedDB) {
        return;
    }

    var _super_pos = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            this.count_sync = 0;
            _super_pos.initialize.call(this, session, attributes);
        },
        sync_without_reload: function (change_detector) {
            change_detector.set_status('connecting');

            var self = this;

            $.when(indexedDB.get('products'), indexedDB.get('customers')).then(function (products, customers) {
                // order_by product
                indexedDB.order_by_in_place(products, ['sequence', 'default_code', 'name'], 'esc');

                // add product
                self.p_super_loaded(self, products);

                // add customer
                self.db.partner_write_date = '';
                self.c_super_loaded(self, customers);

                // re-render products
                self.trigger('change:selectedCategoryId');
                // -end-

                setTimeout(function () {
                    change_detector.set_status('connected');
                }, 500);

                // reset count
                self.count_sync = 0;

            }).fail(function () {
                change_detector.set_status('disconnected', self.count_sync);
            });
        }
    });

    class ChangeDetector extends PosComponent {
        constructor() {
            super(...arguments);
            this.state = useState({ status: 1, msg: 0 });
            this.status = ['connected','connecting','disconnected','warning','error'];
        }

        set_status(status, msg) {
            for (var i = 0; i < this.status.length; i++) {
                $(this.el).find('.jane_' + this.status[i]).addClass('oe_hidden');
            }
            $(this.el).find('.jane_' + status).removeClass('oe_hidden');

            if (msg) {
                $(this.el).find('.jane_msg').removeClass('oe_hidden').text(msg);
            } else {
                $(this.el).find('.jane_msg').addClass('oe_hidden').html('');
            }
        }

        mounted() {
            var self = this;

            this.env.services.bus_service.onNotification(null, function(notifs) {
                self._onNotification(notifs);
            });
            this.env.services.bus_service.startPolling();

            $(this.el).click(function (ev) {
                ev.stopPropagation();
                self.env.pos.sync_without_reload(self);
            });
        }

        _onNotification(notifications) {
            var data = notifications.filter(function (item) {
                return item[0][1] === 'change_detector';
            }).map(function (item) {
                return item[1];
            });

            var p = data.filter(function (item) {
                return item.p;
            });
            var c = data.filter(function (item) {
                return item.c;
            });

            this.on_change(p, c);
        }

        on_change(p, c) {
            if (p.length > 0) {
                this.p_sync_not_reload(p.p);
            }

            if (c.length > 0) {
                this.c_sync_not_reload(c.c);
            }
        }

        p_sync_not_reload(server_version) {
            var self = this;

            var model = self.env.pos.get_model('product.product');

            var client_version = localStorage.getItem('product_index_version');
            if (!/^\d+$/.test(client_version)) {
                client_version = 0;
            }

            if (client_version === server_version) {
                return;
            }

            rpc.query({
                model: 'product.index',
                method: 'sync_not_reload',
                args: [client_version, model.fields]
            }).then(function (res) {
                localStorage.setItem('product_index_version', res['latest_version']);

                // increase count
                self.env.pos.count_sync += res['create'].length + res['delete'].length;

                if (self.env.pos.count_sync > 0) {
                    self.set_status('disconnected', self.env.pos.count_sync);
                }

                indexedDB.open_db().onsuccess = function (ev) {
                    var store = indexedDB.get_object_store('products', ev);
                    _.each(res['create'], function (record) {
                        store.put(record).onerror = function (e) {
                            console.log(e);
                            localStorage.setItem('product_index_version', client_version);
                        }
                    });
                    _.each(res['delete'], function (id) {
                        store.delete(id).onerror = function (e) {
                            console.log(e);
                            localStorage.setItem('product_index_version', client_version);
                        };
                    });
                }
            });
        }

        c_sync_not_reload(server_version) {
            var self = this;

            var model = self.env.pos.get_model('res.partner');

            var client_version = localStorage.getItem('customer_index_version');
            if (!/^\d+$/.test(client_version)) {
                client_version = 0;
            }

            if (client_version === server_version) {
                return;
            }

            rpc.query({
                model: 'customer.index',
                method: 'sync_not_reload',
                args: [client_version, model.fields]
            }).then(function (res) {
                localStorage.setItem('customer_index_version', res['latest_version']);

                self.env.pos.count_sync += res['create'].length + res['delete'].length;

                if (self.env.pos.count_sync > 0) {
                    self.set_status('disconnected', self.env.pos.count_sync);
                }

                indexedDB.open_db().onsuccess = function (ev) {
                    var store = indexedDB.get_object_store('customers', ev);
                    _.each(res['create'], function (record) {
                        store.put(record).onerror = function (e) {
                            console.log(e);
                            localStorage.setItem('customer_index_version', client_version);
                        }
                    });
                    _.each(res['delete'], function (id) {
                        store.delete(id).onerror = function (e) {
                            console.log(e);
                            localStorage.setItem('customer_index_version', client_version);
                        };
                    });
                };
            });
        }
    }

    ChangeDetector.template = 'ChangeDetector';

    Registries.Component.add(ChangeDetector);

    return ChangeDetector;
});