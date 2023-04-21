{
    # App information
    'name': 'Total Line Quantity',
    'version': '14.0.0.0',
    'category': '',
    'summary': 'Total Line Quantity',
    'depends': ['sale_management', 'account', 'purchase'],
    'author': 'Altapete Solutions',
    'maintainer': 'Altapete Solutions',
    'website': 'http://www.altapetesolutions.com/',
    'data': [
        'view/sale_order.xml',
        'view/purchase_order.xml',
        'view/account_move_view.xml',
        'view/stock_picking.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
