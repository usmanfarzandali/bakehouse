# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tot_qty = fields.Float(string='Total Quantity', compute='_compute_sum_quantity')

    @api.depends('order_line.product_uom_qty')
    def _compute_sum_quantity(self):
        for order in self:
            tot_qty = 0
            for line in order.order_line:
                tot_qty += line.product_uom_qty
            order.tot_qty = tot_qty
