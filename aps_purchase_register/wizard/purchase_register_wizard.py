# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class PurchaseRegister(models.TransientModel):
    _name = "purchase.register.wizard"
    _description = "Purchase Register Wizard"

    date_from = fields.Date("From", required=True)
    date_to = fields.Date("To", required=True)
    categ_ids = fields.Many2many(comodel_name='product.category', string='Product Category')
    partner_ids = fields.Many2many(comodel_name='res.partner', string='Partners')
    product_ids = fields.Many2one(comodel_name='product.product', string='Product')
    order_number = fields.Char(string='Purchase Order')
    purchase_type = fields.Selection([
        ('detail', 'Detail Report'),
        ('summary', 'Summary'),
    ], string="Purchase Type", default='detail')
    record_type = fields.Selection([
        ('all', 'All'),
        ('posted', 'Posted'),
    ], string="Records Type", default='posted')

    file = fields.Binary('Download Report')
    name = fields.Char()

    @api.onchange('categ_ids')
    def onchange_vendor(self):
        if self.categ_ids:
            return {'domain': {'product_id': [('categ_id', 'in', self.categ_ids.ids)]}}

    def generate_purchase_register_summary_pdf(self):
        return self.env.ref('aps_purchase_register.purchase_register_summary_report_pdf').with_context(landscape=True).report_action(self,data={'data': self.id})

    def generate_purchase_register_detail_pdf(self):
        return self.env.ref('aps_purchase_register.purchase_register_detail_report_pdf').with_context(
            landscape=True).report_action(self, data={'data': self.id})

    def generate_purchase_register_xlsx(self):
        return self.env.ref('aps_purchase_register.purchase_register_report').report_action(self)

    def generate_purchase_register_summary_xlsx(self):
        
        return self.env.ref('aps_purchase_register.purchase_register_summary_report').report_action(self)
