odoo.define('vpcs_pos_kitchen.Orderline', function(require) {
    'use strict';

    const Orderline = require('point_of_sale.Orderline');
    const Registries = require('point_of_sale.Registries');

    const KitchenOrderline = (Orderline) => 
        class extends Orderline {
            get activeClass() {
                return this.props.line.get_state() != 'done' ? '' : 'active';
            }
        }

    Registries.Component.extend(Orderline, KitchenOrderline);

    return Orderline

});