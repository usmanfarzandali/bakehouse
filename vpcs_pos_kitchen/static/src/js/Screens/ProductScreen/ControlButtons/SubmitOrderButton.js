odoo.define('vpcs_pos_kitchen.SubmitOrderButton', function(require) {
    'use strict';

    const SubmitOrderButton = require('pos_restaurant.SubmitOrderButton');
    const Registries = require('point_of_sale.Registries');

    const KitchenSubmitOrderButton = (SubmitOrderButton) =>
        class extends SubmitOrderButton {
            /**
             * @override
             */
            async onClick() {
                const order = this.env.pos.get_order();
                if (order.hasChangesToPrint()) {
                    const isPrintSuccessful = await order.printChanges();
                    _.each(order.get_orderlines(), function(line) {
                        if (line.get_has_qty_change() && line.printable()) {
                            line.set_state('new');
                            line.set_qty_change(false);
                        }
                    });
                    await order.send_to_kitchen();
                    order.saveChanges();
                    // Comment for not showing error popup
                    // if (isPrintSuccessful) {
                    //     order.saveChanges();
                    // } else {
                    //     await this.showPopup('ErrorPopup', {
                    //         title: 'Printing failed',
                    //         body: 'Failed in printing the changes in the order',
                    //     });
                    // }
                }
            }
        }

    Registries.Component.extend(SubmitOrderButton, KitchenSubmitOrderButton);

    return SubmitOrderButton;
});