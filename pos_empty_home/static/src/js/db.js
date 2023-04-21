odoo.define("pos_empty_home.db", function (require) {
    "use strict";

    var PosDB = require("point_of_sale.DB");

    PosDB.include({
        get_product_by_category: function (category_id) {
            if (window.posmodel.config.iface_empty_home && category_id == 0) {
                return [];
            }
            return this._super.apply(this, arguments);
        },
    });
    return PosDB;
});
