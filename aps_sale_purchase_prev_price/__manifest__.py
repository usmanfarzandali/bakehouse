{
    # App information
    'name': 'Sale Purchase History',
    'version': '14.0.0.0',
    'category': 'Purchase',
    'summary': 'Sale Purchase History',
    'depends':['purchase','sale_management'],
    'author': 'Altapete Solutions',
    'maintainer': 'Altapete Solutions',
    'website': 'http://www.altapetesolutions.com/',
    'data': [
        'views/purchase.xml',
        'views/sale.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
