odoo.define('vpcs_pos_kitchen.KitchenScreen', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');
    const { useState } = owl.hooks;
    var session = require("web.session");
    var iface_pos_tone = _.contains(session.module_list, 'vpcs_pos_kitchen_tone.KitchenTones');


    class KitchenScreen extends PosComponent {
        constructor() {
            super(...arguments);
            this.state = useState({mode: 'list'});
            this.total_orders = -1;
            this.last_update_rows = [];
        }
        get orders() {
            var self = this;
            let tones = false;
            if(iface_pos_tone) {
                tones = true;
            }
            let OrdersList = [];
            let Orders = this.env.pos.db.pos_synch_all_parsed(this.env.pos.db.synch_orders);
            _.each(Orders, function(order) {
                const has_products = _.filter(order.orderlines, function(line) {
                    return line.product;
                });
                if (has_products) {
                    OrdersList.push(order);
                }
            });
            let bell = false;
            if (this.total_orders != -1 && this.total_orders < OrdersList.length && this.props.KitchenScreen ==  true) {
                bell = true;
            } else {
                let last_update_rows = this.last_update_rows;
                const KitchenScreen = this.props.KitchenScreen;
                _.each(OrdersList, function(row) {
                    let _torder = _.findWhere(last_update_rows, {
                        'name': row.name
                    });
                    if (!_torder) {
                        return;
                    } else if (_torder.orderlines.length < row.orderlines.length) {
                        if (KitchenScreen == true) {
                            bell = true;
                        }
                        return;
                    }
                    _.each(row.orderlines, function(line) {
                        var _tline = _.findWhere(_torder.orderlines, {
                            'id': line.id
                        });
                        if (_tline && _tline.qty < line.qty) {
                            if (KitchenScreen == true) {
                                bell = true;
                            }
                            return;
                        }
                    });
                    if (bell) {
                        return
                    }
                });
            }
            if (bell) {
                this.trigger('play-kitchen-sound', 'tin', tones);
            }
            this.total_orders = OrdersList.length;
            this.last_update_rows = OrdersList;
            return OrdersList
        }
        async _fetchOrders() {
            await this.env.pos.db.reload_orders();
            const orders = this.orders;
            this.render();
        }
        willPatch() {
            posbus.off('ticket-button-clicked', this);
            posbus.off('render-kitchen', this);
        }
        patched() {
            posbus.on('ticket-button-clicked', this, this.render, '', false);
            posbus.on('render-kitchen', this, this.renderKitchenScreen);
        }
        mounted() {
            posbus.on('ticket-button-clicked', this, this.render, '', false);
            posbus.on('render-kitchen', this, this.renderKitchenScreen);
            this._fetchOrders();
        }
        willUnmount() {
            posbus.off('ticket-button-clicked', this);
            posbus.off('render-kitchen', this);
        }
        renderKitchenScreen() {
            this._fetchOrders();
        }
        get iface_is_kitchen() {
            return this.env.pos.config.iface_is_kitchen;
        }
        get get_session_name() {
            return this.env.pos.config.display_name;
        }
    }

    KitchenScreen.template = 'KitchenScreen';

    Registries.Component.add(KitchenScreen);

    return KitchenScreen;
});