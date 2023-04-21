# -*- coding: utf-8 -*-
{
    'name': "Point of Sale - Empty Home",
    'summary': """Point of Sale - Hide products if no category is selected""",
    'description': """Point of Sale - Hide products if no category is selected""",
    'version': '14.0.0.1',
    "category": "Point of Sale",
    'author': "Altapete Solutions",
    'website': "http://altapetesolutions.com/",
    'maintainer': 'Altapete Solutions',
    'company': 'Altapete Solutions',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'point_of_sale',
    ],
    'data': [
        "views/assets.xml",
        "views/pos_config.xml",
    ],
    'qweb': [
        "static/src/xml/pos_empty_home.xml",
    ],
    'demo': [
        "demo/pos_empty_home.xml",
    ],
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 0,
    'currency': 'PKR',
}
