from odoo import models, api, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pur_approval_amount = fields.Float(string="Purchase Approval Amount")
