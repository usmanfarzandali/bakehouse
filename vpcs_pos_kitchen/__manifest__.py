# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'POS Kitchen',
    'version': '14.0.0.1',
    'category': 'POS',
    'summary': 'POS Kitchen Bus Notification',
    'sequence': 0,
    'description': """
    POS Kitchen
    ===========
    This module provides pos kitchen screen functionality
    for manage the kitchen orders more efficient way.

    Features :-
    ===========
    More attractive and user friendly.
    Bus Notification Concept.
    Support modify order and apply new changes in kitchen screen after place order.
    Easily identify product based on category color.
    Sync product states.
    """,
    'author': 'VperfectCS',
    'maintainer': 'VperfectCS',
    'website': 'http://www.vperfectcs.com',
    'depends': ['pos_restaurant'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_assets_common.xml',
        'views/pos_order_synch_view.xml',
        'views/pos_category_view.xml',
        'views/pos_config_view.xml'
    ],
    'qweb': [
        'static/src/xml/color_widget.xml',
        'static/src/xml/Chrome.xml',
        'static/src/xml/ChromeWidgets/TicketButton.xml',
        'static/src/xml/Screens/ProductScreen/Orderline.xml',
        'static/src/xml/Screens/ProductScreen/ControlButtons/KitchenScreenButton.xml',
        'static/src/xml/Screens/ProductScreen/ControlButtons/OrderPriorityButton.xml',
        'static/src/xml/Screens/KitchenScreen/KitchenOrderStateButton.xml',
        'static/src/xml/Screens/KitchenScreen/KitchenOrder.xml',
        'static/src/xml/Screens/KitchenScreen/KitchenScreen.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 99,
    'currency': 'EUR',
}
