# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    tot_qty = fields.Float(string='Total Quantity', compute='_compute_sum_quantity')

    @api.depends('invoice_line_ids.quantity')
    def _compute_sum_quantity(self):
        for invoice in self:
            tot_qty = 0
            for line in invoice.invoice_line_ids:
                tot_qty += line.quantity
            invoice.tot_qty = tot_qty
