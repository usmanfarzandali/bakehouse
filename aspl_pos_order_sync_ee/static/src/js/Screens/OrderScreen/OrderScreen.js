odoo.define('aspl_pos_order_sync_ee.OrderScreen', function (require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const IndependentToOrderScreen = require('point_of_sale.IndependentToOrderScreen');
    const { useListener } = require('web.custom_hooks');
    const { debounce } = owl.utils;
    const { posbus } = require('point_of_sale.utils');
    var rpc = require('web.rpc');

    class OrderScreen extends IndependentToOrderScreen {
        constructor() {
            super(...arguments);
            useListener('close-order-screen', this.close);
            useListener('click-delete', () => this.clickDeleteOrder(event));
            useListener('click-edit', () => this.click_edit_order(event));
            useListener('click-print', () => this.click_reprint(event));
            useListener('search', this._onSearch);
            this.searchDetails = {};
            this.filter = null;
            this._initializeSearchFieldConstants();
        }

        _onSearch(event) {
            const searchDetails = event.detail;
            Object.assign(this.searchDetails, searchDetails);
            this.render();
        }
        get DbOrders() {
            return this.env.pos.db.get_orders_list();
        }
        get clients() {
            if (this.state.query && this.state.query.trim() !== '') {
                return this.env.pos.db.search_orders(this.state.query.trim());
            }
        }
        get filteredOrders() {
            const filterCheck = (order) => {
                if (this.filter && this.filter !== 'All Orders') {
                    const screen = order.get_screen_data();
                    return this.filter === this.constants.screenToStatusMap[screen.name];
                }
                return true;
            };
            const { fieldValue, searchTerm } = this.searchDetails;
            const fieldAccessor = this._searchFields[fieldValue];
            const searchCheck = (order) => {
                if (!fieldAccessor) return true;
                const fieldValue = fieldAccessor(order);
                if (fieldValue === null) return true;
                if (!searchTerm) return true;
                return fieldValue && fieldValue.toString().toLowerCase().includes(searchTerm.toLowerCase());
            };
            const predicate = (order) => {
                return filterCheck(order) && searchCheck(order);
            };
            return this.DbOrders.filter(predicate);
        }

        get searchBarConfig() {
            return {
                searchFields: this.constants.searchFieldNames,
                filter: { show: true, options: this.filterOptions },
            };
        }

        get filterOptions() {
            return ['All Orders'];
        }
        get _searchFields() {
            var fields = {
                'Order/Ref': (order) => order.name,
                'Receipt/Ref': (order) => order.pos_reference,
                'Order Date (YYYY-MM-DD)': (order) => moment(order.creation_date).format('YYYY-MM-DD hh:mm A'),
                'Salesman': (order) => order.salesman_id[1],
                'Order State': (order) => order.state,
                 Customer: (order) => order.partner_id[1],
            };
            return fields;
        }

        _initializeSearchFieldConstants() {
            this.constants = {};
            Object.assign(this.constants, {
                searchFieldNames: Object.keys(this._searchFields),
            });
        }

        clickDeleteOrder(event){
            var self = this;
            var order_id = event.detail.order_id;
            var order_to_be_remove = self.env.pos.db.get_orders_list_by_id(order_id);
            if (order_to_be_remove && order_to_be_remove.lines.length > 0) {
                var params = {
                    model: 'pos.order',
                    method: 'unlink',
                    args: [order_to_be_remove.id],
                }
                rpc.query(params, {async: false}).then(function(result){});
            }
            var orders_list = self.env.pos.db.get_orders_list();
            orders_list = _.without(orders_list, _.findWhere(orders_list, { id: order_to_be_remove.id }));
            var orderFiltered = orders_list.filter(order => order.state == "draft").length;
            this.trigger('reload-order-count',{ orders_count:orderFiltered});
            self.env.pos.db.add_orders(orders_list)
            self.env.pos.db.add_draft_orders(orderFiltered);
            this.render();
        }

        click_edit_order(event){
            var self = this;
            const {order_id} = event.detail;
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
                        })
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

        click_reprint(event) {
            var self = this;
            var selectedOrder = this.env.pos.get_order();
            console.log(selectedOrder);
            var order_id = event.detail.order_id;
            selectedOrder.destroy();
            console.log(selectedOrder);
            selectedOrder = this.env.pos.get_order();
            var result = self.env.pos.db.get_orders_list_by_id(order_id);
            console.log(result);
            if (result.partner_id && result.partner_id[0]) {
                var partner = self.env.pos.db.get_partner_by_id(result.partner_id[0])
                if(partner){
                    selectedOrder.set_client(partner);
                }
            }
            if(result.payment_ids.length > 0){
                self.get_journal_from_order(result.payment_ids);
            }
            var journal = self.get_journal_from_order(result.payment_ids);
            selectedOrder.set_amount_return(Math.abs(result.amount_return));
            selectedOrder.set_date_order(result.date_order);
            selectedOrder.set_pos_reference(result.pos_reference);
// ======================================================================================
            selectedOrder.name = result.pos_reference;
            selectedOrder.barcode = result.barcode;
// ======================================================================================
            if(result.lines.length > 0){
                var order_lines = self.get_orderlines_from_order(result.lines).then(function(order_lines){
                    if(order_lines.length > 0){
                        _.each(order_lines, function(line){
                            var product = self.env.pos.db.get_product_by_id(Number(line.product_id[0]));
                            if(product){
                                selectedOrder.add_product(product, {
                                    quantity: line.qty,
                                    discount: line.discount,
                                    price: line.price_unit,
                                })
                            }
                        })
                    }
                    selectedOrder.set_order_id(order_id);
                    self.showScreen('ReceiptScreen');
                });
            }

        }

        get_journal_from_order(statement_ids) {
            var self = this;
            var order = self.env.pos.get_order();
            var PaymentPromise = new Promise(function(resolve, reject){
                var params = {
                    model: 'pos.payment',
                    method: 'search_read',
                    domain: [['id', 'in', statement_ids]],
                }
                rpc.query(params, {async: false}).then(function(statements){
                    if(statements.length > 0){
                        resolve(statements);
                    }
                });
            })
            PaymentPromise.then(function(statements){
                var order_statements = []
                _.each(statements, function(statement){
                    if(statement.amount > 0){
                        order_statements.push({
                            amount: statement.amount,
                            payment_method: statement.payment_method_id[1],
                        })
                    }
                });
                if(order_statements){
                    order.set_journal(order_statements);
                }else{
                    console.log("Connection lost");
                }
             })
        }

         async click_reorder(order_id){
            var self = this;
            var result = self.env.pos.db.get_orders_list_by_id(order_id);
            var flag = false;
            var order_lines = await self.get_orderlines_from_order(result.lines)
            const { confirmed,payload: selectedLines } = await self.showPopup('ReOrderPopup55', {
                                title: self.env._t('Products'), orderlines : order_lines});

            if(confirmed) {
                var currentOrder = self.env.pos.get_order();
                var selected_line_ids = _.pluck(selectedLines, 'id');
                if(selected_line_ids){
                    currentOrder.destroy();
                    currentOrder = self.env.pos.get_order();
                    selected_line_ids.map(function(id){
                        var line = _.find(selectedLines, function(obj) { return obj.id == id});
                        var qty = line.qty;
                        if(line && qty > 0){
                            if(line.product_id && line.product_id[0]){
                                var product = self.env.pos.db.get_product_by_id(line.product_id[0]);
                                if(product){
                                    flag = true;
                                    currentOrder.add_product(product, {
                                        quantity: qty,
                                    });
                                }
                            }
                        }
                    });
                    if(flag){
                        if(result.partner_id[0]){
                            let partner = self.env.pos.db.get_partner_by_id(result.partner_id[0]);
                            currentOrder.set_client(partner);
                        }else{
                            currentOrder.set_client(null);
                        }
                        self.render();
                        self.showScreen('ProductScreen');
                    }
                }
            }
         }

    }

    OrderScreen.template = 'OrderScreen';

    Registries.Component.add(OrderScreen);

    return OrderScreen;
});

