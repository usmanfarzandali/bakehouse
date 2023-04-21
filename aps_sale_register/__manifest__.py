# -*- coding: utf-8 -*-
{
    'name': "Sale Register Report",
    'summary': """Sale Register Report""",
    "website": "http://www.altapetesolution.com",
    "author": "Altapete Solution",
    'category': 'Sale',
    'version': '14.0.0.1',
    'depends': ['base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_pdf_template_summary.xml',
        'reports/report_pdf_template_detail.xml',
        'reports/report.xml',
        'wizard/sale_register_wizard.xml',
    ],
}