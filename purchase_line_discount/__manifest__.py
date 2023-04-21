# -*- coding: utf-8 -*-
{
    'name': "SW - Purchase Order Lines Discount",
    'summary': """
        Add Percentage Discount (%) to your Purchase Orders and Requests for Quotations
        """,
    'description': """
        Adds new "Discount (%)" field in POL that applies discount to the POL and affects the inventory valuation. Odoo by default doesn't allow for discounts in the PO.
    """,
    'author': "Smart Way Business Solutions",
    'website': "https://www.smartway.co",
    'category': 'Purchases',
    'version': '1.3',
    'depends': ['base', 'purchase'],
    'data': [
        'views/purchase_order.xml',
        "views/assets.xml"
    ],
    'images':  ["static/description/image.png"],
}
