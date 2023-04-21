odoo.define('purchase_line_discount.product_discount', function (require) {
    "use strict";

    const BasicFields = require('web.basic_fields');
    const FieldsRegistry = require('web.field_registry');

    const PurchaseProductDiscountWidget = BasicFields.FieldFloat.extend({

        /**
         * Override changes at a discount.
         *
         * @override
         * @param {OdooEvent} ev
         *
         */
        async reset(record, ev) {
            if (ev && ev.data.changes && ev.data.changes.discount >= 0) {
               this.trigger_up('open_discount_wizard_purchase');
            }
            this._super(...arguments);
        },
    });

    FieldsRegistry.add('product_purchase_discount', PurchaseProductDiscountWidget);

    return ProductDiscountWidget;

});
