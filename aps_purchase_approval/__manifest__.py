{
    # App information
    'name': 'Purchase Approval',
    'version': '14.0.0.0',
    'category': 'Purchase',
    'summary': 'Purchase Approval Cycle',
    'depends':['purchase'],
    'author': 'Altapete Solutions',
    'maintainer': 'Altapete Solutions',
    'website': 'http://www.altapetesolutions.com/',
    'data': [
        'security/purchase_groups.xml',
        'views/res_partner.xml',
        'views/purchase.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
