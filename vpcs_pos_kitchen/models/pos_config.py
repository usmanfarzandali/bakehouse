# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models 

class PosConfig(models.Model):
    _inherit = 'pos.config'

    iface_is_kitchen = fields.Boolean('Default Kitchen View', help="Set as default screen.")
    iface_btn_kitchen = fields.Boolean('Show Kitchen Button', help="Allow to show kitchen screen.")
    iface_btn_priority = fields.Boolean('Order Priority')