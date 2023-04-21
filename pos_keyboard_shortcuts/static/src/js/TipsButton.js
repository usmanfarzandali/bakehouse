odoo.define('pos_keyboard_shortcuts.TipsButton', function(require) {
    'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { posbus } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');


    class TipsButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        onClick() {
            Gui.showPopup("PosShortcutsPopup", {
                title: this.env._t('Shortcut Tips (F2)'),
                body: this.env._t(''),
            });
        }
    }

    TipsButton.template = 'TipsButton';
    ProductScreen.addControlButton({
        component: TipsButton,
        condition: function() {
            return this.env.pos;
        },
    });
    Registries.Component.add(TipsButton);
    return TipsButton;

});
