# -*- coding: utf-8 -*-
{
    'name': "Purchase Register Report",
    'summary': """Purchase Register Report""",
    "website": "http://www.altapetesolution.com",
    "author": "Altapete Solution",
    'category': 'Purchase',
    'version': '14.0.0.1',
    'depends': ['base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report.xml',
        'reports/pdf_report_template.xml',
        'reports/pdf_report_detail.xml',
        'wizard/purchase_register_wizard.xml',
    ],
}