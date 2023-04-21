# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Category(models.Model):
    _inherit = 'pos.category'

    color = fields.Char('Color')