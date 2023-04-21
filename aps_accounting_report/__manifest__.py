# -*- coding: utf-8 -*-
{
    'name': "Supplier Movement Report",
    'summary': """Supplier Movement Report""",
    "website": "http://www.altapetesolution.com",
    "author": "Altapete Solution",
    'category': 'Accounting',
    'version': '14.0.0.0',
    'depends': ['base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/pdf_template_ledger.xml',
        'report/pdf_template_supplier.xml',
        'wizard/supplier_movement_wizard.xml',
        'wizard/partner_ledger_wizard.xml',
    ],
}