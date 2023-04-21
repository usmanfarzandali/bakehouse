odoo.define('vpcs_pos_kitchen.KitchenScreenButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class kitchenScreenButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
         async onClick() {
            this.showScreen('KitchenScreen', {'KitchenScreen': true});
         };
    }
    kitchenScreenButton.template = 'KitchenScreenButton';

    ProductScreen.addControlButton({
        component: kitchenScreenButton,
        condition: function() {
            return this.env.pos.config.iface_btn_kitchen;
        },
    });

    Registries.Component.add(kitchenScreenButton);

    return kitchenScreenButton;

});