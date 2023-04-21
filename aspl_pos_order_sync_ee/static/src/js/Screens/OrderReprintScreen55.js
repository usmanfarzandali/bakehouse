odoo.define('aspl_pos_order_sync_ee.OrderReprintScreen55', function (require) {
	'use strict';

	const ReceiptScreen = require('point_of_sale.ReceiptScreen');
	const Registries = require('point_of_sale.Registries');

	const OrderReprintScreen55 = (ReceiptScreen) => {
		class OrderReprintScreen55 extends ReceiptScreen {
			constructor() {
				super(...arguments);
			}
//			back() {
////				this.props.resolve({ confirmed: true, payload: null });
//				this.trigger('close-temp-screen');
//			}
		}
		OrderReprintScreen55.template = 'OrderReprintScreen55';
		return OrderReprintScreen55;
	};

	Registries.Component.addByExtending(OrderReprintScreen55, ReceiptScreen);

	return OrderReprintScreen55;
});
