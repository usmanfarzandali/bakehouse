# -*- coding: utf-8 -*-

{
    'name': 'Pos Multi Barcode Options by kamal',
    'version': '2.0.4',
    'category': 'Product',
    'sequence': 6,
    'author': 'Kamil',
    'summary': "Pos multi barcode option module allows you give create multiple barcode of single product with different options." ,
    'description': """

=======================

Pos multi barcode option module allows you give create multiple barcode of single product with different options.

""",
    'depends': ['point_of_sale', 'aspl_pos_order_sync_ee'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/barcode_rule.xml',
        'views/templates.xml'
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/adds.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 29,
    'currency': 'EUR',
}