odoo.define('aspl_pos_order_sync_ee.ProductScreen', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const POSOrdersScreen = require('pos_orders_all.POSOrdersScreen');
    const Registries = require('point_of_sale.Registries');

    const { useListener } = require('web.custom_hooks');
    const { useState, useRef } = owl.hooks;
    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t = core._t;

    const ProductScreenInherit = (ProductScreen) =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
                useListener('close-draft-screen', this.closeScreen);
                useListener('click-edit', () => this.click_edit_order(event));
            }

            closeScreen(){
                this.trigger('show-orders-panel');
            }

            async _onClickPay() {
                if(this.env.pos.user.pos_user_type === "salesman" && this.env.pos.config.enable_order_sync){
                    let currentOrder = this.env.pos.get_order();
                    var order_str =  currentOrder.get_is_modified_order() ? " Modify " : " Create Draft ";
                    const { confirmed } = await this.showPopup('CreateDraftOrderPopup', {
                        title: this.env._t('Draft Order'),
                        body: this.env._t('Do You Want To' + order_str +'Order?'),
                    });
                    if (confirmed){
                        this.env.pos.get_order().set_salesman_id(this.env.pos.user.id);
                        this.env.pos.push_orders(this.env.pos.get_order());

                        var order = this.env.pos.get_order();
                        var orderlines = this.env.pos.get_order().get_orderlines();
                        var receipt = this.env.pos.get_order().getOrderReceiptEnv().receipt;

                        receipt.date.localestring = (new Date()).toLocaleString();
                        receipt.name = receipt.name.replace('Order ', '')

//                        console.log(receipt.name);
//                        console.log(receipt.date.localestring);
//                        console.log(receipt);
//                        console.log(order);
//                        console.log(orderlines);

//                        this.showScreen('ReceiptScreen');
                        this.showScreen('OrderReprintScreen55', {'receipt': receipt, 'order': order});
                    }
                }else{
                    this.showScreen('PaymentScreen');
                }
            }

            async _setValue(val) {
                var discount_limit = this.env.pos.user.discount_limit;
                var managers = this.env.pos.config.pos_managers_ids;
                if(this.env.pos.config.enable_operation_restrict){
                    if(this.state.numpadMode === 'discount'){
                        if(val > discount_limit){
                            if(_.contains(managers,this.env.pos.user.id)){
                                this.currentOrder.get_selected_orderline().set_discount(val);
                                return;
                            }
                            if(managers.length > 0){
                                const { confirmed,payload: enteredPin } = await this.showPopup('AuthenticationPopup', {
                                    title: this.env._t('Authentication'),
                                });
                                if(confirmed){
                                    const userFiltered = this.env.pos.users.filter(user => managers.includes(user.id));
                                    var result_find = _.find(userFiltered, function (user) {
                                        return user.custom_security_pin === enteredPin || user.barcode === enteredPin;
                                    });
                                    if(result_find){
                                        this.currentOrder.get_selected_orderline().set_discount(val);
                                        return;
                                    }else{
                                        alert(_t('Please Enter correct PIN/Barcode!'));
                                        return;
                                    }
                                }
                            }else{
                                alert(_t('Please Contact Your Manager!'));
                                return;
                            }
                        }
                    }
                }
                super._setValue(val);
            }

            quick_delete(order_id){
                var self = this;
                var order_to_be_remove = self.env.pos.db.get_orders_list_by_id(order_id);
                if (order_to_be_remove) {
                    var params = {
                        model: 'pos.order',
                        method: 'unlink',
                        args: [order_to_be_remove.id],
                    }
                    rpc.query(params, {async: false}).then(function(result){});
                }
                var orders_list = self.env.pos.db.get_orders_list();
                orders_list = _.without(orders_list, _.findWhere(orders_list, { id: order_to_be_remove.id }));
                var orderFiltered = orders_list.filter(order => order.state == "draft");
                self.env.pos.db.add_orders(orders_list);
                self.env.pos.db.add_draft_orders(orderFiltered);
                this.trigger('reload-order-count',{ orders_count:orderFiltered.length});
                self.render();
            }

//            async click_reorder(order_id){

//                var self = this;
//                var result = self.env.pos.db.get_orders_list_by_id(order_id);
//                var flag = false;
//                var order_lines = await self.get_orderlines_from_order(result.lines)
//
////                const { confirmed,payload: selectedLines } = await self.showPopup('ReOrderPopup55', {
////                                    title: self.env._t('Products'), orderlines : order_lines});
////                console.log(order_lines, selectedLines)
////              if popup than order_lines replaced with selectedLines
//                if(order_lines) {
//                    var currentOrder = self.env.pos.get_order();
//                    var selected_line_ids = _.pluck(order_lines, 'id');
////                    console.log(order_lines, selected_line_ids)
//
//                    if(selected_line_ids){
////                        currentOrder.destroy();
//                        currentOrder = self.env.pos.get_order();
//                        selected_line_ids.map(function(id){
//                            var line = _.find(order_lines, function(obj) { return obj.id == id});
//                            var qty = line.qty;
//                            if(line && qty > 0){
//                                if(line.product_id && line.product_id[0]){
//                                    var product = self.env.pos.db.get_product_by_id(line.product_id[0]);
//                                    if(product){
//                                        flag = true;
//                                        currentOrder.add_product(product, {
//                                            quantity: qty,
//                                        });
//                                    }
//                                }
//                            }
//                        });
//                        if(flag){
//                            if(result.partner_id[0]){
//                                let partner = self.env.pos.db.get_partner_by_id(result.partner_id[0]);
//                                currentOrder.set_client(partner);
//                            }else {
//                                currentOrder.set_client(null);
//                            }
////                            self.quick_delete(order_id);
//                            self.render();
//                            self.showScreen('ProductScreen');
//                        }
//                    }
//                }
//             }

        async _barcodeProductAction(code) {
//            console.log(this.env.pos.db.orders_list[0].barcode);
//            console.log(this.env.pos.db.orders_list);
//            console.log(this.env.pos.db.draft_orders_list);
//            console.log(this.env.pos.db);
//            console.log(code.code);
//            console.log(this.env.pos.db.draft_orders_list[0].barcode);
            var len = this.env.pos.db.draft_orders_list.length;
            var order_id, order_line;
            for(var i=0;i<len;i++){
                if(this.env.pos.db.draft_orders_list[i].barcode == code.code){
                    order_id = this.env.pos.db.draft_orders_list[i].id;
                    order_line = this.env.pos.db.draft_orders_list[i].lines[0];
                }
            }
//            console.log(order_id, order_line);

            var pos_multi_op = this.env.pos.multi_barcode_options;
            var qty, bar_name, price, unit, price_set;
            for(var i=0;i<pos_multi_op.length;i++) {
                if(pos_multi_op[i].name == code.code) {
                    var qty         = pos_multi_op[i].qty;
                    var bar_name    = pos_multi_op[i].name;
                    var price       = pos_multi_op[i].price;
                    var unit        = pos_multi_op[i].unit[0];
                    var price_set   = true;
                }
            }
            if(bar_name) {
//                console.log('bar_name::', bar_name);
                const product = this.env.pos.db.get_product_by_barcode(code.base_code)
                if (!product) {
                    return this._barcodeErrorAction(code);
                }
                const options = await this._getAddProductOptions(product);
                // Do not proceed on adding the product when no options is returned.
                // This is consistent with _clickProduct.
                if (!options) return;

                // update the options depending on the type of the scanned code
                if (code.type === 'price') {
                    Object.assign(options, { price: code.value });
                } else if (code.type === 'weight') {
                    Object.assign(options, {
                        quantity: code.value,
                        merge: false,
                    });
                } else if (code.type === 'discount') {
                    Object.assign(options, {
                        discount: code.value,
                        merge: false,
                    });
                }
                var bar_state = true;
                this.currentOrder.add_product(product,  options, bar_state);

                var line = this.currentOrder.get_last_orderline();
                var pos_multi = this.env.pos.multi_barcode_options;
                for(var i=0;i<pos_multi.length;i++){
                    if(pos_multi[i].name == code.code){
                        line.set_quantity(qty);
                        line.set_unit_price(price);
                        line.set_pro_uom(unit);
                        line.price_manually_set = price_set;
                    }
                }
            } else if(order_id){
//                console.log('order_id::', order_id);
                var self = this;
                var result = self.env.pos.db.get_orders_list_by_id(order_id);
                if(result && result.lines.length > 0){
    //                var selectedOrder = this.env.pos.get_order();
    //                selectedOrder.destroy();
                    var selectedOrder = this.env.pos.get_order();
                    if (result.partner_id && result.partner_id[0]) {
                        var partner = self.env.pos.db.get_partner_by_id(result.partner_id[0])
                        if(partner){
                            selectedOrder.set_client(partner);
                        }
                    }
                    selectedOrder.set_pos_reference(result.pos_reference);
                    selectedOrder.set_order_id(order_id);
                    selectedOrder.server_id = order_id;
                    selectedOrder.set_sequence(result.name);
                    if(result.salesman_id && result.salesman_id[0]){
                        selectedOrder.set_salesman_id(result.salesman_id[0]);
                    }
                    var order_lines = self.get_orderlines_from_order(result.lines).then(function(order_lines) {
                        if(order_lines && order_lines.length > 0){
                            _.each(order_lines, function(line){
                                var product = self.env.pos.db.get_product_by_id(Number(line.product_id[0]));
                                selectedOrder.add_product(product, {
                                    quantity: line.qty,
                                    discount: line.discount,
                                    price: line.price_unit,
                                });
//                                if(event.detail.operation == 'payment'){
//                                 self.showScreen('PaymentScreen',{'order_id':order_id});
//                                }
//                                if(event.detail.operation == 'edit'){
//                                    selectedOrder.set_is_modified_order(true);
//                                    self.showScreen('ProductScreen');
//                                }
                                selectedOrder.set_is_modified_order(true);
                                self.render();
                                self.showScreen('ProductScreen');
                            })
                        }
                    })
                }
            } else {
                const product = this.env.pos.db.get_product_by_barcode(code.base_code);
                if (!product) {
                    return this._barcodeErrorAction(code);
                }
                const options = await this._getAddProductOptions(product);
                // Do not proceed on adding the product when no options is returned.
                // This is consistent with _clickProduct.
                if (!options) return;

                // update the options depending on the type of the scanned code
                if (code.type === 'price') {
                    Object.assign(options, {
                        price: code.value,
                        extras: {
                            price_manually_set: true,
                        },
                    });
                } else if (code.type === 'weight') {
                    Object.assign(options, {
                        quantity: code.value,
                        merge: false,
                    });
                } else if (code.type === 'discount') {
                    Object.assign(options, {
                        discount: code.value,
                        merge: false,
                    });
                }
                this.currentOrder.add_product(product,  options)
            }
    }

        click_edit_order(event){
            var self = this;
            console.log(event);
            console.log(event.detail);
            const {order_id} = event.detail;
            var result = self.env.pos.db.get_orders_list_by_id(order_id);
            if(result && result.lines.length > 0){
//                var selectedOrder = this.env.pos.get_order();
//                selectedOrder.destroy();
                var selectedOrder = this.env.pos.get_order();
                if (result.partner_id && result.partner_id[0]) {
                    var partner = self.env.pos.db.get_partner_by_id(result.partner_id[0])
                    if(partner){
                        selectedOrder.set_client(partner);
                    }
                }
                selectedOrder.set_pos_reference(result.pos_reference);
                selectedOrder.set_order_id(order_id);
                selectedOrder.server_id = order_id;
                selectedOrder.set_sequence(result.name);
                if(result.salesman_id && result.salesman_id[0]){
                    selectedOrder.set_salesman_id(result.salesman_id[0]);
                }
                var order_lines = self.get_orderlines_from_order(result.lines).then(function(order_lines) {
                    if(order_lines && order_lines.length > 0){
                        _.each(order_lines, function(line){
                            var product = self.env.pos.db.get_product_by_id(Number(line.product_id[0]));
                            selectedOrder.add_product(product, {
                                quantity: line.qty,
                                discount: line.discount,
                                price: line.price_unit,
                            });
                            if(event.detail.operation == 'payment'){
                                self.showScreen('PaymentScreen',{'order_id':order_id});
                            }
                            if(event.detail.operation == 'edit'){
                                selectedOrder.set_is_modified_order(true);
                                self.showScreen('ProductScreen');
                            }
                            self.render();
                            self.showScreen('ProductScreen');
                        })
                    }
                })
            }
        }

            quick_pay(order_id){
                var self = this;
                var result = self.env.pos.db.get_orders_list_by_id(order_id);
                if(result && result.lines.length > 0){
                    var selectedOrder = this.env.pos.get_order();
                    selectedOrder.destroy();
                    var selectedOrder = this.env.pos.get_order();
                    if (result.partner_id && result.partner_id[0]) {
                        var partner = self.env.pos.db.get_partner_by_id(result.partner_id[0])
                        if(partner){
                            selectedOrder.set_client(partner);
                        }
                    }
                    selectedOrder.set_pos_reference(result.pos_reference);
                    selectedOrder.set_order_id(order_id);
                    selectedOrder.server_id = result.id;

                    selectedOrder.set_sequence(result.name);
                    if(result.salesman_id && result.salesman_id[0]){
                        selectedOrder.set_salesman_id(result.salesman_id[0]);
                    }
                    var order_lines = self.get_orderlines_from_order(result.lines).then(function(order_lines) {
                        if(order_lines && order_lines.length > 0){
                            _.each(order_lines, function(line){
                                var product = self.env.pos.db.get_product_by_id(Number(line.product_id[0]));
                                selectedOrder.add_product(product, {
                                    quantity: line.qty,
                                    discount: line.discount,
                                    price: line.price_unit,
                                });
                            });
                            self.trigger('show-orders-panel');
                            self.showScreen('PaymentScreen',{'order_id':order_id});
                        }
                    })
                }
            }

            get_orderlines_from_order(line_ids){
                var self = this;
                var orderLines = [];
                return new Promise(function (resolve, reject) {
                    rpc.query({
                        model: 'pos.order.line',
                        method: 'search_read',
                        domain: [['id', 'in', line_ids]],
                    }).then(function (order_lines) {
                        resolve(order_lines);
                    })
                });
            }
        };

    Registries.Component.extend(ProductScreen, ProductScreenInherit);

    return ProductScreen;
});
