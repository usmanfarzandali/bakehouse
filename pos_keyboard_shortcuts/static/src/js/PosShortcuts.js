odoo.define('pos_keyboard_shortcuts.PosShortcuts', function (require) {
    "use strict";
    var core = require('web.core');
    var PosShortcuts = core.Class.extend({
        init: function (attributes) {
            var pos = attributes.pos;
//            console.log('=============Pass=============');
            document.addEventListener('keydown', (event) => {
//                console.log('=============Pass=============', event.which);
                if(!$(document).find("div.search-box input").is(":focus") && !$($(document).find(".product-screen")[0]).hasClass('oe_hidden')){
//                    if(event.ctrlKey && event.which == 79) {
                    if(event.which == 76) {
                        event.preventDefault();
                        // Product-Screen click on " L " button to Delete All Orders from Cart:
                        pos.get_order().remove_orderline(pos.get_order().get_orderlines());
                    }
                }
            }, false);
        },
    });
    return PosShortcuts;
});
