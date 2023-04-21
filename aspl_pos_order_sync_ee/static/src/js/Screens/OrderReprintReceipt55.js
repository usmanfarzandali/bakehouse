odoo.define('aspl_pos_order_sync_ee.OrderReprintReceipt55', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');

	class OrderReprintReceipt55 extends PosComponent {
		constructor() {
			super(...arguments);
		}
		
		get receiptBarcode(){
            var order = this.env.pos.get_order();
            $("#barcode_print22").barcode(
                order.barcode, // Value barcode (dependent on the type of barcode)
                "code128" // type (string)
            );
            return true;
        }
	}
	OrderReprintReceipt55.template = 'OrderReprintReceipt55';

	Registries.Component.add(OrderReprintReceipt55);

	return OrderReprintReceipt55;
});
