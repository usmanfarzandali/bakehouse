# -*- coding: utf-8 -*-
{
    'name': 'Manufacturing Product Barcode Printing',
    'version': '14.0',
    'summary': 'Manufacturing Product label with Company name, Product name, Price/Offer Price, Pack date, Lot num, Exp date',
    'description': """Include Company name, product name, price, pack date, lot num, exp date """,
    'category': 'mrp',
    'author': "Altapete Solutions",
    'website': 'https://www.altapetesolutions.com',
    'depends' : ['mrp'],
    'data': [
        'reports/product_label_inherit.xml',
        'reports/reports.xml'


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
