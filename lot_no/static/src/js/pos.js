odoo.define('lot_no.POSProductScreen', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { useState } = owl.hooks;
    const { parse } = require('web.field_utils');

    const models = require('point_of_sale.models');
    models.load_models({
        model: 'stock.production.lot',
        fields: ['name','product_id'],
        domain: function(self){ },
        loaded: function(self,list_lot){
                self.list_lot = list_lot;
            },
    });

    const POSProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            async _getAddProductOptions(product) {
                let price_extra = 0.0;
                let draftPackLotLines, weight, description, packLotLinesToEdit;

                if (this.env.pos.config.product_configurator && _.some(product.attribute_line_ids, (id) => id in this.env.pos.attributes_by_ptal_id)) {
                    let attributes = _.map(product.attribute_line_ids, (id) => this.env.pos.attributes_by_ptal_id[id])
                                      .filter((attr) => attr !== undefined);
                    let { confirmed, payload } = await this.showPopup('ProductConfiguratorPopup', {
                        product: product,
                        attributes: attributes,
                    });

                    if (confirmed) {
                        description = payload.selected_attributes.join(', ');
                        price_extra += payload.price_extra;
                    } else {
                        return;
                    }
                }

                // Gather lot information if required.
                if (['serial', 'lot'].includes(product.tracking) && (this.env.pos.picking_type.use_create_lots || this.env.pos.picking_type.use_existing_lots)) {
                    const isAllowOnlyOneLot = product.isAllowOnlyOneLot();
//                    console.log(product);
                    var list_lot = this.env.pos.list_lot;
                    var lotNumber= [];
                    for(var i=0;i<list_lot.length;i++){
//                        console.log(this.env.pos.list_lot[i].name);
//                        console.log(this.env.pos.list_lot[i].product_id[0]);
                        if(product.id == this.env.pos.list_lot[i].product_id[0]){
                            lotNumber.push(this.env.pos.list_lot[i].name);
                        }
                    }
//                    console.log(lotNumber);
//                    console.log(this.env.pos.list_lot);
                    if (isAllowOnlyOneLot) {
                        if(lotNumber){
                            packLotLinesToEdit = lotNumber;
                        } else {
                            packLotLinesToEdit = [];
                        }
                    } else {
                        const orderline = this.currentOrder
                            .get_orderlines()
                            .filter(line => !line.get_discount())
                            .find(line => line.product.id === product.id);
                        if (orderline) {
                            packLotLinesToEdit = orderline.getPackLotLinesToEdit();
                        } else {
                            packLotLinesToEdit = [];
                        }
                    }
                    const { confirmed, payload } = await this.showPopup('EditListPopup', {
                        title: this.env._t('Lot/Serial Number(s) Required'),
                        isSingleItem: isAllowOnlyOneLot,
                        array: packLotLinesToEdit,
                    });
                    if (confirmed) {
                        // Segregate the old and new packlot lines
                        const modifiedPackLotLines = Object.fromEntries(
                            payload.newArray.filter(item => item.id).map(item => [item.id, item.text])
                        );
                        const newPackLotLines = payload.newArray
                            .filter(item => !item.id)
                            .map(item => ({ lot_name: item.text }));
                        draftPackLotLines = { modifiedPackLotLines, newPackLotLines };
                    } else {
                        // We don't proceed on adding product.
                        return;
                    }
                }

                // Take the weight if necessary.
                if (product.to_weight && this.env.pos.config.iface_electronic_scale) {
                    // Show the ScaleScreen to weigh the product.
                    if (this.isScaleAvailable) {
                        const { confirmed, payload } = await this.showTempScreen('ScaleScreen', {
                            product,
                        });
                        if (confirmed) {
                            weight = payload.weight;
                        } else {
                            // do not add the product;
                            return;
                        }
                    } else {
                        await this._onScaleNotAvailable();
                    }
                }

                return { draftPackLotLines, quantity: weight, description, price_extra };
            }
        }
    Registries.Component.extend(ProductScreen, POSProductScreen);
});
