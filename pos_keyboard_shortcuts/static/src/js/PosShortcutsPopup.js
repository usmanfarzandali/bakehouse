odoo.define('pos_keyboard_shortcuts.PosShortcutsPopup', function(require) {
    'use strict';
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const PosComponent = require('point_of_sale.PosComponent');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require('web.custom_hooks');
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { useState } = owl.hooks;

    class PosShortcutsPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }
    }

    //Create products popup
    PosShortcutsPopup.template = 'PosShortcutsPopup';
    PosShortcutsPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
    };

    Registries.Component.add(PosShortcutsPopup);
    return PosShortcutsPopup;
});