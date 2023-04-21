# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class SupplierMovement(models.TransientModel):
    _name = "supplier.movement.wizard"
    _description = "Supplier Movement Wizard"

    date_from = fields.Date("From", required=True)
    date_to = fields.Date("To", required=True)
    partner_ids = fields.Many2many(comodel_name='res.partner', string='Partners')
    partner_type = fields.Selection([
        ('both', 'Both'),
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ], string='Partner Type', default='both')
    companies = fields.Many2many(comodel_name='res.company', string='Company')

    file = fields.Binary('Download Report')
    name = fields.Char()

    def generate_supplier_movement_xlsx(self):
        return self.env.ref('aps_accounting_report.supplier_movement_report').report_action(self)

    def generate_supplier_movement_pdf(self):
        data = {'date_start': self.date_from, 'date_to': self.date_to, 'partner_ids': [self.partner_ids], 'partner_type': self.partner_type, }
        return self.env.ref('aps_accounting_report.supplier_movement_report_pdf').report_action(self,data={'wizard':data})
