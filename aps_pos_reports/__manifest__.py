# -*- coding: utf-8 -*-
{
    'name':  'APS POS Reports',
    'summary': """
        APS All in One Reports:
            -Sales Details Report
            -Sales Summary Report
            -Ongoing Session Report
            -Posted Session Report
            -Top Selling Customer/Product/Category Report
            -Pos Profit-Loss Report
            -Pos Payment Report
    """,
    'description': """
        APS All in One Reports:
            -Sales Details Report
            -Sales Summary Report
            -Ongoing Session Report
            -Posted Session Report
            -Top Selling Customer/Product/Category Report
            -Pos Profit-Loss Report
            -Pos Payment Report
    """,
    'sequence': -100,
    'version': '2.0.4',
    "category": "Point of Sale",
    'author': "Altapete Solutions",
    'website': "http://altapetesolutions.com/",
    'maintainer': 'Altapete Solutions',
    'company': 'Altapete Solutions',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sales_summary_report.xml',
        'wizard/pos_sale_summary.xml',
        'wizard/x_report_view.xml',
        'wizard/z_report_view.xml',
        'wizard/top_selling.xml',
        'wizard/top_selling_report.xml',
        'wizard/profit_loss_report.xml',
        'wizard/profit_loss.xml',
        'wizard/pos_payment_report.xml',
        'wizard/pos_payment.xml',
    ],
    'qweb': [],
    'demo': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 0,
    'currency': 'PKR',
}
