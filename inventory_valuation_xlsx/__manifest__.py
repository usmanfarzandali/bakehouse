# -*- coding: utf-8 -*-
{
    'name': "Inventory Valuation Report",
    'summary': """
    Witholding Report
    """,
    "website": "http://www.altapetesolution.com",
    "author": "Altapete Solution",
    'category': 'stock',
    'version': '14.0.0.0',
    'depends': ['base', 'report_xlsx', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/inventory_summary_pdf.xml',
        'report/product_stock_pdf.xml',
        'report/inventory_valuation_location_wise.xml',
        'report/inv_val_stock_pdf.xml',
        'report/inv_valuation_summary.xml',
        'wizard/inventory_valuation.xml',


    ],
}