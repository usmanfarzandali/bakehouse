odoo.define('aspl_pos_order_sync_ee.OrdersIconChrome', function(require) {
    'use strict';

    const { useState } = owl;
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class OrdersIconChrome extends PosComponent {
        constructor() {
            super(...arguments);
        }
        async onClick() {
            if(this.env.pos.config.enable_notification){
                this.trigger('show-orders-panel');
            }
        }

        get count() {
            return this.props.orderCount;
        }
    }
    OrdersIconChrome.template = 'OrdersIconChrome';

    Registries.Component.add(OrdersIconChrome);

    return OrdersIconChrome;
});
