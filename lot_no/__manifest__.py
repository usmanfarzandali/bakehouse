# -*- coding: utf-8 -*-
{
    'name': "POS Autocomplete Lot\Serial Number",
    'summary': """ 
        POS Lot\Serial Number for Autocompletion 
    """,
    'description': """ 
        POS Lot\Serial Number for Autocompletion 
    """,
    'author': "Altapete Solutions",
    'website': "http://altapetesolutions.com/",
    'category': 'point_of_sale',
    'version': '14.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
}
