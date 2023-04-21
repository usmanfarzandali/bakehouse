# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'POS Order Synchronization (Enterprise)',
    'version': '2.0.4',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'summary': 'POS Order sync between Salesman and Cashier',
    'description': "Allow salesperson to only create draft order and send draft order to Cashier for payment",
    'category': 'Point Of Sale',
    'website': 'http://www.acespritech.com',
    'depends': ['base', 'point_of_sale'],
    'price': 25.00,
    'currency': 'EUR',
    'images': [
        'static/description/main_screenshot.png',
    ],
    'data': [
        'views/pos_assets.xml',
        'views/point_of_sale.xml',
        'views/res_users_view.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'qweb': [
        'static/src/xml/screens/ChromeWidgets/OrdersIconChrome.xml',
        'static/src/xml/screens/ProductScreen/ControlButtons/OrderScreenButton.xml',
        'static/src/xml/screens/ProductScreen/ProductScreen.xml',
        'static/src/xml/screens/OrderScreen/OrderScreen.xml',
        'static/src/xml/screens/OrderScreen/PopupProductLines.xml',
        'static/src/xml/Popups/CreateDraftOrderPopup.xml',
        'static/src/xml/Popups/ReOrderPopup.xml',
        'static/src/xml/Popups/AuthenticationPopup.xml',
        'static/src/xml/Chrome.xml',
        'static/src/xml/screens/ReceiptScreen/OrderReceipt.xml',
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
