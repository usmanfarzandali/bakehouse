{
    'name': 'Odoo POS Promotional Scheme',
    'version': '14.0.2',
    'category': 'Point Of Sale',
    'sequence': 6,
    'summary': 'Touch-screen Interface for Shops  point of sale pos promotional scheme Odoo pos coupons and vouchers pos retail odoo point of sale point of sale retail odoo point of sale pos app',
    'description': """
Odoo POS Promotional Scheme
===========================
This module shows the basic processes involved in the selected modules and in the sequence they occur.

**Note:** This applies to the modules containing modulename_process.xml.

**e.g.** product/process/product_process.xml.
<keywords>
POS
point of sale
pos promotional scheme
Odoo pos
pos coupons and vouchers
pos retail
odoo point of sale
point of sale retail
odoo point of sale
pos app
    """,
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': 'www.pragtech.co.in',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/scheme_view.xml',
        'views/templates.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'price': 50,
    'currency': 'EUR',
    'license': 'OPL-1',
    'images': ['images/Animated-POS-Promotional-scheme.gif'],
    'live_test_url': 'https://www.pragtech.co.in/company/proposal-form.html?id=103&name=Odoo-Promotional-scheme-Management',
    'installable': True,
    'application': True,
    'auto_install': False,
}
