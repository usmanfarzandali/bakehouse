# -*- coding: utf-8 -*-

{
    "name": "APS Custom POS",
    "summary": "APS Custom POS",
    "version": "15.0.0.0",
    "author": "Altapete Solution",
    "category": "Point of Sale",
    "website": "www.altapetesolutions.com",
    'depends': ['base', 'point_of_sale'],
    "data": [],
    "qweb": ["static/src/xml/pos_receipt.xml"],
    "installable": True,
    "auto_install": False,
    "application": True,
    'assets': {
        'web.assets_qweb': [
            'aps_pos_custom_receipt/static/src/xml/**/*',
        ],
    },
}
