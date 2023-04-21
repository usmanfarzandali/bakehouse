odoo.define('pos_keyboard_shortcuts.PosProductScreen', function(require) {
    'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { posbus } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');

    const PosShortcuts = require('pos_keyboard_shortcuts.PosShortcuts');

    const PosProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            _PosKey = new PosShortcuts({'pos': this.env.pos});
        };

    /* Function For Product Screen Key Down Events */
    function Product_Screen_Key_Down_Events(event){
        if(!$($(document).find(".product-screen")[0]).hasClass('oe_hidden')){
            if(event.which == 13){
                // Enter for Product on Order Line
                $($(document).find("div.product-screen")[0]).find("div.product-list article.highlight").click();
            } else if(event.which == 37){
                // Left Arrow Product
                if($($(document).find("div.product-screen")[0]).find("div.product-list article.highlight").length > 0){
                    var elem = $($(document).find("div.product-screen")[0]).find("div.product-list article.highlight");
                    elem.removeClass("highlight");
                    elem.prev("article").addClass("highlight").focus();
                } else {
                    var payMethodLength = $($(document).find("div.product-screen")[0]).find("div.product-list article").length;
                    if(payMethodLength > 0){
                        $($($(document).find("div.product-screen")[0]).find("div.product-list article")[payMethodLength-1]).addClass('highlight').focus();
                    }
                }
            } else if(event.which == 39){
                // Right Arrow Product
                if($($(document).find("div.product-screen")[0]).find("div.product-list article.highlight").length > 0){
                    var elem = $($(document).find("div.product-screen")[0]).find("div.product-list article.highlight");
                    elem.removeClass("highlight");
                    elem.next("article").addClass("highlight").focus();
                } else {
                    var payMethodLength = $($(document).find("div.product-screen")[0]).find("div.product-list article").length;
                    if(payMethodLength > 0){
                        $($($(document).find("div.product-screen")[0]).find("div.product-list article")[0]).addClass('highlight').focus();
                    }
                }
            }
        }
        if(!$($(document).find(".product-screen")[0]).hasClass('oe_hidden')){
            if(event.which == 113){
                // Product-Screen click on "F2" button to ShortcutTips :
                $(document).find("div.product-screen div.leftpane button#tipsButton").trigger("click");
            }
        }
//        console.log(!document.querySelector('div.search-bar-portal div.search-box input') === document.activeElement)
        if(!(document.querySelector('div.search-bar-portal div.search-box input') === document.activeElement) && !$($(document).find(".product-screen")[0]).hasClass('oe_hidden')){
            if(event.which == 81) {
                // Product-Screen click on "Q" button to Quantity:
                $($(document).find("div.product-screen div.leftpane button.mode-button")[0]).trigger("click");
            } else if(event.which == 68){
                // Product-Screen click on "D" button to Discount:
                $($(document).find("div.product-screen div.leftpane button.mode-button")[1]).trigger("click");
            } else if(event.which == 80){
                // Product-Screen click on "P" button to Price:
                $($(document).find("div.product-screen div.leftpane button.mode-button")[2]).trigger("click");
            } else if(event.which == 67) {
                // Product-Screen click on "C" button to Open Customer Screen:
                $(document).find("div.product-screen div.leftpane button.set-customer").trigger("click");
            } else if(event.which == 32) {
                // Product-Screen click on "Spacebar" button to Open Payment Screen:
                event.preventDefault();
                $(document).find("div.product-screen div.leftpane button.pay").trigger("click");
            }else if(event.which == 38) {
                // Product-Screen click on "Up Arrow" button to up direction in OrderLine Cart:
                $(document).find("div.product-screen ul.orderlines li.selected").prev('li.orderline').click();
            } else if(event.which == 40) {
                // Product-Screen click on "Down Arrow" button to down direction in OrderLine Cart:
                $(document).find("div.product-screen ul.orderlines li.selected").next('li.orderline').click();
            } else if(event.which == 83){
                // Product-Screen click on "S" button to Search Bar:
                $(document).find("div.search-bar-portal div.search-box input").focus();
                event.preventDefault();
            }
        }
    }

    /* Payment Screen Key Down Events */
    function Payment_Screen_Key_Down_Events(event){
//            !$($(document).find("div.payment-screen")[0]).hasClass('oe_hidden')
//            $($(document).find("div.payment-screen")[0]).length
        if(!$($(document).find("div.payment-screen")[0]).hasClass('oe_hidden') && $($(document).find("div.payment-screen")[0]).length){
            if (event.which == 27) {
                // Payment-Screen click on "Esc" button to Back Home Screen:
                $($(document).find("div.payment-screen")[0]).find("div.top-content div.back").trigger('click');
            } else if(event.which == 67) {
                // Payment-Screen click on "c" button to Customer Screen:
                $($(document).find("div.payment-screen")[0]).find("div.payment-buttons div.customer-button div.button").trigger('click');
            } else if (event.which == 73) {
                // Payment-Screen click on "i" button to Invoice Button Clicked:
                $($(document).find("div.payment-screen")[0]).find("div.payment-buttons div.js_invoice").trigger('click');
            } else if(event.which == 33) {
                // Payment-Screen paymentmethods click on "Page Up" button :
                if($($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight").length > 0){
                    var elem = $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight");
                    elem.removeClass("highlight");
                    elem.prev("div.paymentmethod").addClass("highlight");
                } else {
                    var payMethodLength = $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod").length;
                    if(payMethodLength > 0){
                        $($($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod")[payMethodLength-1]).addClass('highlight');
                    }
                }
            } else if(event.which == 34) {
                // Payment-Screen paymentmethods click on "Page Down" button :
                if($($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight").length > 0){
                    var elem = $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight");
                    elem.removeClass("highlight");
                    elem.next("div.paymentmethod").addClass("highlight");
                } else {
                    var payMethodLength = $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod").length;
                    if(payMethodLength > 0){
                        $($($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod")[0]).addClass('highlight');
                    }
                }
            } else if(event.which == 32) {
                // Payment-Screen Select a paymentmethods click on "Space" button :
                event.preventDefault();
                $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.highlight").trigger("click");
                $($(document).find("div.payment-screen")[0]).find("div.paymentmethods div.paymentmethod").removeClass("highlight");
            } else if(event.which == 38) {
                // Payment-Screen Selected paymentlines click on "Arrow Up" button :
                if($($(document).find("div.payment-screen")[0]).find("div.paymentlines div.selected").length > 0){
                    $($(document).find("div.payment-screen")[0]).find("div.paymentlines div.selected").prev("div.paymentline").trigger("click");
                }else{
                    var payLineLength = $($(document).find("div.payment-screen")[0]).find("div.paymentlines div.paymentline").length;
                    if(payLineLength > 0){
                        $($($(document).find("div.payment-screen")[0]).find("div.paymentlines div.paymentline")[payLineLength-1]).trigger('click');
                    }
                }
            } else if(event.which == 40) {
                //Payment-Screen Selected paymentlines click on "Arrow Down" button :
                if($($(document).find("div.payment-screen")[0]).find("div.paymentlines div.selected").length > 0){
                    var elem = $($(document).find("div.payment-screen")[0]).find("div.paymentlines div.selected").next("div.paymentline").trigger("click");
                }else{
                    var payLineLength = $($(document).find("div.payment-screen")[0]).find("div.paymentlines div.paymentline").length;
                    if(payLineLength > 0){
                        $($($(document).find("div.payment-screen")[0]).find("div.paymentlines div.paymentline")[0]).trigger('click');
                    }
                }
            } else if(event.which == 46) {
                // Payment-Screen Selected paymentlines Delete Button Click:
                event.preventDefault();
                $($(document).find("div.payment-screen")[0]).find("div.paymentlines div.selected div.delete-button").click();
            }else if(event.which == 13){
                // Payment-Screen click on "Enter" button to go Receipt Screen:
                event.preventDefault();
                $($(document).find("div.payment-screen")[0]).find("div.top-content div.highlight").trigger("click");
            }
        }
    }

    /* Client-List Screen Key Down Events */
    function Client_List_Screen_Key_Down_Events(event){
//        !$($(document).find("div.clientlist-screen")[0]).hasClass('oe_hidden')
        if(!(document.querySelector('div.top-content div.searchbox-client input') === document.activeElement) && $($(document).find("div.clientlist-screen")[0]).length){
            if (event.which == 27) {
                // Customer-Screen click on "Esc" button to back :
                $($(document).find("div.clientlist-screen")[0]).find("div.top-content div.back").trigger('click');
            } else if(event.which == 83) {
                // Customer-Screen click on "S" button to Search it:
                $(document).find("div.top-content div.searchbox-client input").focus();
                event.preventDefault();
            } else if(event.which == 38) {
                // Customer-Screen click on "Arrow Up" button :
                if($(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight").length > 0){
                    $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight").prev("tr.client-line").click();
                }else{
                    var clientLineLength = $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.client-line").length;
                    if(clientLineLength > 0){
                        $($(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.client-line")[clientLineLength-1]).click();
                    }
                }
            } else if(event.which == 40) {
                // Customer-Screen click on "Arrow Down" button :
                if($(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight").length > 0){
                    $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight").next("tr.client-line").click();
                }else{
                    var clientLineLength = $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.client-line").length;
                    if(clientLineLength > 0){
                        $($(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.client-line")[0]).click();
                    }
                }
            } else if(event.which == 13) {
                // Customer-Screen click on "Enter" button to Select a Customer:
                if(!$(document).find("div.clientlist-screen div.top-content div.next").hasClass('oe_hidden')){
                    $(document).find("div.clientlist-screen div.top-content div.next").click();
                    event.preventDefault();
                }
            } else if(event.which == 78) {
                // Customer-Screen click on " n " button to Create New Customer:
                $(document).find("div.clientlist-screen div.screen-content div.top-content div.new-customer").click();
            } else if(event.which == 69) {
                // Customer-Screen click on " e " button to Edit Customer Form:
                $(document).find("div.clientlist-screen table.client-list tbody.client-list-contents tr.highlight button.edit-client-button").click();
            }
        }
    }

    /* Receipt Screen Key Down Events */
    function Receipt_Screen_Key_Down_Events(event){
        if($($(document).find("div.receipt-screen")[0]).length){
            if(event.which == 73){
                // Receipt-Screen click on "i" button to sent email:
                $($(document).find("div.receipt-screen")[0]).find("div.input-email button.send").trigger("click");
            } else if(event.which == 82){
                // Receipt-Screen click on "r" button to print receipt:
                $($(document).find("div.receipt-screen")[0]).find("div.print").trigger("click");
            } else if(event.which == 13){
                // Receipt-Screen click on "Enter" button to Home/ Page:
                $($(document).find("div.receipt-screen")[0]).find("div.top-content div.next").trigger("click");
            }
        }
    }

    document.addEventListener('keydown', (event) => {
//        var name = event.key;
//        var code = event.code;
//        var num = event.which;
//        console.log(name, code, num, event);
//        console.log(event.which);
//        alert(`Key pressed ${name} \r\n Key code value: ${code} \r\n Key num value: ${num}`);

        /* Product Screen Key Down Events */
        Product_Screen_Key_Down_Events(event);

        /* Payment Screen Key Down Events */
        Payment_Screen_Key_Down_Events(event);

        /* Client-List Screen Key Down Events */
        Client_List_Screen_Key_Down_Events(event);

        /* Receipt Screen Key Down Events */
        Receipt_Screen_Key_Down_Events(event);

        }, false);

    Registries.Component.extend(ProductScreen, PosProductScreen);
});
