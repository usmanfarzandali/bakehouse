odoo.define('vpcs_pos_kitchen.TicketButton', function (require) {
    'use strict';

    const TicketButton = require('point_of_sale.TicketButton');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');
    const { useRef } = owl.hooks;

    const KitchenTicketButton = (TicketButton) =>
        class extends TicketButton {
            constructor() {
                super(...arguments);
                this.ticketButtonRef = useRef('ticket-button-ref');
            }
            onClick() {
                if(this.props.isKitchenScreenShown) {
                    posbus.trigger('ticket-button-clicked');
                }else{
                    super.onClick();
                }
            }
            willPatch() {
            if(this.props.isKitchenScreenShown){
                this.ticketButtonRef.el.style.display = 'none';
            }else{
                this.ticketButtonRef.el.style.display = 'flex';
            }
            super.willPatch();
        }
        patched() {
            if(this.props.isKitchenScreenShown){
                this.ticketButtonRef.el.style.display = 'none';
            }else{
                this.ticketButtonRef.el.style.display = 'flex';
            }
            super.patched();
        }
        }

    Registries.Component.extend(TicketButton, KitchenTicketButton);

    return TicketButton;
});