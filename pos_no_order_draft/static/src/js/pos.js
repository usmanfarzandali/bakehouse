odoo.define('pos_no_order_draft.pos', function (require) {
    'use strict';

    const { useState } = owl;
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const HeaderButton = require('point_of_sale.HeaderButton');

    const PosHeaderButton = (HeaderButton) =>
        class extends HeaderButton {
            onClick() {
                if (!this.confirmed) {
                    if(this.set_no_order_draft() == 0 ){
                        this.state.label = 'Confirm';
                        this.confirmed = setTimeout(() => {
                            this.state.label = 'Close';
                            this.confirmed = null;
                        }, 2000);
                    } else {
                        alert('Please, Proceed or Remove Unpaid Orders!');
                    }
                } else {
                    this.trigger('close-pos');
                }
            }

            set_no_order_draft(){
                var orderList = this.env.pos.get_order_list();
                var lenList = this.env.pos.get_order_list().length;
                var listAmountTotal = 0.0;
                for(var i=0; i<lenList; i++){
                    //console.log('Order(',i+1,') = ', orderList[i])
                    listAmountTotal += orderList[i].get_total_with_tax()
                }
                //console.log('listAmountTotal = ', listAmountTotal)
                return listAmountTotal;
            }
        };

    Registries.Component.extend(HeaderButton, PosHeaderButton);
    return HeaderButton;
});
