odoo.define('vpcs_pos_kitchen.KitchenOrderStateButton', function(require){
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');

    class KitchenOrderStateButton extends PosComponent {
        constructor() {
            super(...arguments);
            this.state_by_name = {
                'new': 'New',
                'Cooking': 'Cooking',
                'ready to serve': 'Ready To Serve',
                'done': 'Done'
            }
        }
        get_state_name(state){
            return this.state_by_name[state];
        }
        get highlight_new() {
            return this.props.orderline.state !== 'new' ? '' : 'active';
        }
        get highlight_cooking() {
            return this.props.orderline.state !== 'Cooking' ? '' : 'active';
        }
        get highlight_ready_to_serve() {
            return this.props.orderline.state !== 'ready to serve' ? '' : 'active';
        }
        get highlight_done() {
            return this.props.orderline.state !== 'done' ? '' : 'active';
        }
        async _ClickOrderlineState(order, orderline, state) {
            await this.env.pos.db.pos_orderline_state(order.uid, orderline.id, state);
            posbus.trigger('render-kitchen');
        }
    }

    KitchenOrderStateButton.template = 'KitchenOrderStateButton';

    Registries.Component.add(KitchenOrderStateButton);

    return KitchenOrderStateButton
});