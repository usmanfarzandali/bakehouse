odoo.define('vpcs_pos_kitchen.TicketScreen', function(require) {
    'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');
    const { posbus } = require('point_of_sale.utils');

    const KitchenTicketScreen = (TicketScreen) =>
        class extends TicketScreen {
            async deleteOrder(order) {
                const screen = order.get_screen_data();
                if (['ProductScreen', 'PaymentScreen'].includes(screen.name) && order.get_orderlines().length > 0) {
                    const { confirmed } = await this.showPopup('ConfirmPopup', {
                        title: 'Existing orderlines',
                        body: `${order.name} has total amount of ${this.getTotal(
                            order
                        )}, are you sure you want delete this order?`,
                    });
                    if (!confirmed) return;
                }
                if (order) {
                    var uid = order.uid;
                    order.destroy({ reason: 'abandon' });
                    this.env.pos.db.remove_order(uid);
                }
                posbus.trigger('order-deleted');
            }
        }

    Registries.Component.extend(TicketScreen, KitchenTicketScreen);

    return TicketScreen;
});