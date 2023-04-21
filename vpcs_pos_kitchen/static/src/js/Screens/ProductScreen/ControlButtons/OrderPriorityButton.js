odoo.define('vpcs_pos_kitchen.OrderPriorityButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    class orderPriorityButton extends PosComponent {
        constructor() {
            super(...arguments);
            this._currentOrder = this.env.pos.get_order();
            this._currentOrder.orderlines.on('change', this.render, this);
            this.env.pos.on('change:selectedOrder', this._updateCurrentOrder, this);
        }
        willUnmount() {
            this._currentOrder.orderlines.off('change', null, this);
            this.env.pos.off('change:selectedOrder', null, this);
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        get orderPriority() {
            return this.currentOrder ? this.currentOrder.get_priority() : 'normal';
        }
        captureChange(event) {
            const order = this.env.pos.get_order();
            if (!order) return;
            order.set_priority(event.target.value);
        }
        _updateCurrentOrder(pos, newSelectedOrder) {
            this._currentOrder.orderlines.off('change', null, this);
            if (newSelectedOrder) {
                this._currentOrder = newSelectedOrder;
                this._currentOrder.orderlines.on('change', this.render, this);
            }
        }
    }
    orderPriorityButton.template = 'OrderPriorityButton';

    ProductScreen.addControlButton({
        component: orderPriorityButton,
        condition: function() {
            return this.env.pos.config.iface_btn_priority;
        },
    });

    Registries.Component.add(orderPriorityButton);

    return orderPriorityButton;
});