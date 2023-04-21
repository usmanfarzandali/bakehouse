odoo.define('pos_multi_barcodes.PosResProductScreen', function (require) {
"use strict";
    var models = require('point_of_sale.models');
    var PosDB = require('point_of_sale.DB');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');


    models.load_fields('product.product',['pos_multi_barcode_option']);
    models.load_models([{
        model: 'pos.multi.barcode.options',
        fields: ['name','product_id','qty','price','unit'],
        loaded: function(self,result){
            self.db.add_barcode_options(result);
            self.multi_barcode_options = result;
        },
    }],{'after': 'pos.category'});

    PosDB.include({
        init: function(options){
            var self = this;
            this.product_barcode_option_list = {};
            this._super(options);

        },
        add_products: function(products){
            var self = this;
            this._super(products); 
            
            for(var i = 0, len = products.length; i < len; i++){
                var product = products[i];
                if(product.pos_multi_barcode_option){
                    var barcod_opt = self.product_barcode_option_list;
                    for(var k=0;k<barcod_opt.length;k++){
                        for(var j=0;j<product.pos_multi_barcode_option.length;j++){
                            if(barcod_opt[k].id == product.pos_multi_barcode_option[j]){
                                this.product_by_barcode[barcod_opt[k].name] = product;
                            }
                        }
                    }
                }
            }
        },
        add_barcode_options:function(barcode){
            this.product_barcode_option_list = barcode;
        },

    });

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.call(this,attr,options);
            this.new_uom = '';
        },
        set_pro_uom: function(uom_id){
            this.new_uom = this.pos.units_by_id[uom_id];
            this.trigger('change',this);
        },
        get_unit: function(){
            var unit_id = this.product.uom_id;
            if(!unit_id){
                return undefined;
            }
            unit_id = unit_id[0];
            if(!this.pos){
                return undefined;
            }
            return this.new_uom == ''  ? this.pos.units_by_id[unit_id] : this.new_uom;
        },
        export_as_JSON: function(){
            var unit_id = this.product.uom_id;
            var json = _super_orderline.export_as_JSON.call(this);
            json.product_uom = this.new_uom == '' ? unit_id[0] : this.new_uom.id;
            return json;
        },
        init_from_JSON: function(json){
            _super_orderline.init_from_JSON.apply(this,arguments);
            this.new_uom = json.new_uom;
        },
    });

    var _super_order = models.Order.prototype;
    var exports = {};
    models.Order = models.Order.extend({
        initialize: function(attributes, options) {
            _super_order.initialize.apply(this, arguments);
            var self = this;
            options  = options || {};
        },
        add_product: function(product, options, bar_state=false){
            if(this._printed){
                this.destroy();
                return this.pos.get_order().add_product(product, options);
            }
            this.assert_editable();
            options = options || {};
            var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});
            this.fix_tax_included_price(line);

            if(options.quantity !== undefined){
                line.set_quantity(options.quantity);
            }

            if (options.price_extra !== undefined){
                line.price_extra = options.price_extra;
                line.set_unit_price(line.product.get_price(this.pricelist, line.get_quantity(), options.price_extra));
                this.fix_tax_included_price(line);
            }

            if(options.price !== undefined){
                line.set_unit_price(options.price);
                this.fix_tax_included_price(line);
            }

            if(options.lst_price !== undefined){
                line.set_lst_price(options.lst_price);
            }

            if(options.discount !== undefined){
                line.set_discount(options.discount);
            }

            if (options.description !== undefined){
                line.description += options.description;
            }

            if(options.extras !== undefined){
                for (var prop in options.extras) {
                    line[prop] = options.extras[prop];
                }
            }
            if (options.is_tip) {
                this.is_tipped = true;
                this.tip_amount = options.price;
            }

//            console.log(line);
//            console.log(line.product.pos_multi_barcode_option.length);
//            console.log(line.description);
//            if(line.product.pos_multi_barcode_option.length <= 0) {
//                var to_merge_orderline;
//                for (var i = 0; i < this.orderlines.length; i++) {
//                    if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
//                        to_merge_orderline = this.orderlines.at(i);
//                    }
//                }
//                if (to_merge_orderline){
//                    to_merge_orderline.merge(line);
//                    this.select_orderline(to_merge_orderline);
//                } else {
//                    this.orderlines.add(line);
//                    this.select_orderline(this.get_last_orderline());
//                }
//            } else {

//            console.log(line);
//            console.log(bar_state);
            if(bar_state == true) {
                this.orderlines.add(line);
                this.select_orderline(this.get_last_orderline());
            } else {
//                console.log(line.description);
                var to_merge_orderline;
                for (var i = 0; i < this.orderlines.length; i++) {
                    if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
                        to_merge_orderline = this.orderlines.at(i);
                    }
                }
                if (to_merge_orderline){
                    to_merge_orderline.merge(line);
                    this.select_orderline(to_merge_orderline);
                } else {
                    this.orderlines.add(line);
                    this.select_orderline(this.get_last_orderline());
                }
            }
//            }

//            var to_merge_orderline;
//            for (var i = 0; i < this.orderlines.length; i++) {
//                if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
//                    to_merge_orderline = this.orderlines.at(i);
//                }
//            }
//            if (to_merge_orderline){
//                to_merge_orderline.merge(line);
//                this.select_orderline(to_merge_orderline);
//            } else {
//                this.orderlines.add(line);
//                this.select_orderline(this.get_last_orderline());
//            }

            if (options.draftPackLotLines) {
                this.selected_orderline.setPackLotLines(options.draftPackLotLines);
            }
            if (this.pos.config.iface_customer_facing_display) {
                this.pos.send_current_order_to_customer_facing_display();
            }
        },
    });

    const PosResProductScreen = (ProductScreen) =>
        class extends ProductScreen {
//            async _barcodeProductAction(code) {
//                var pos_multi_op = this.env.pos.multi_barcode_options;
//                for(var i=0;i<pos_multi_op.length;i++) {
//                    if(pos_multi_op[i].name == code.code) {
//                        var qty         = pos_multi_op[i].qty;
//                        var bar_name    = pos_multi_op[i].name;
//                        var price       = pos_multi_op[i].price;
//                        var unit        = pos_multi_op[i].unit[0];
//                        var price_set   = true;
//                    }
//                }
//                if(bar_name) {
////                    console.log(bar_name);
//                    const product = this.env.pos.db.get_product_by_barcode(code.base_code)
//                    if (!product) {
//                        return this._barcodeErrorAction(code);
//                    }
//                    const options = await this._getAddProductOptions(product);
//                    // Do not proceed on adding the product when no options is returned.
//                    // This is consistent with _clickProduct.
//                    if (!options) return;
//
//                    // update the options depending on the type of the scanned code
//                    if (code.type === 'price') {
//                        Object.assign(options, { price: code.value });
//                    } else if (code.type === 'weight') {
//                        Object.assign(options, {
//                            quantity: code.value,
//                            merge: false,
//                        });
//                    } else if (code.type === 'discount') {
//                        Object.assign(options, {
//                            discount: code.value,
//                            merge: false,
//                        });
//                    }
//                    this.currentOrder.add_product(product,  options);
//
//                    var line = this.currentOrder.get_last_orderline();
//                    var pos_multi = this.env.pos.multi_barcode_options;
//                    for(var i=0;i<pos_multi.length;i++){
//                        if(pos_multi[i].name == code.code){
//                            line.set_quantity(qty);
//                            line.set_unit_price(price);
//                            line.set_pro_uom(unit);
//                            line.price_manually_set = price_set;
//                        }
//                    }
//                } else {
//                    const product = this.env.pos.db.get_product_by_barcode(code.base_code)
//                    if (!product) {
//                        return this._barcodeErrorAction(code);
//                    }
//                    const options = await this._getAddProductOptions(product);
//                    // Do not proceed on adding the product when no options is returned.
//                    // This is consistent with _clickProduct.
//                    if (!options) return;
//
//                    // update the options depending on the type of the scanned code
//                    if (code.type === 'price') {
//                        Object.assign(options, { price: code.value });
//                    } else if (code.type === 'weight') {
//                        Object.assign(options, {
//                            quantity: code.value,
//                            merge: false,
//                        });
//                    } else if (code.type === 'discount') {
//                        Object.assign(options, {
//                            discount: code.value,
//                            merge: false,
//                        });
//                    }
//                    this.currentOrder.add_product(product,  options);
//                }
//            }
        };

    Registries.Component.extend(ProductScreen, PosResProductScreen);
});

