from odoo import models, api, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    approval_amount = fields.Float(string="Sale Approval Amount")
