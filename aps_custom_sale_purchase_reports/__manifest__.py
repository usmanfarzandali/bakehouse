# -*- coding: utf-8 -*-
{
    'name' : 'Modified Sale Purchase Reports',
    'version' : '14.0.0.1',
    'summary': 'Modified Sale Purchase Reports',
    'description': """Modified Sale Purchase Reports""",
    'category': 'Purchase',
    'website': 'https://www.altapetesolutions.com',
    'depends' : ['base'],
    'data': [
        'reports/reports.xml',
        'reports/sale_report_inherit.xml',
        'reports/purchase_order_inherit.xml',
        'reports/invoice_inherit.xml',
        'reports/delivery_slip_inherit.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
