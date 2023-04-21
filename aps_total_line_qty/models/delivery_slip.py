# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliverySlip(models.Model):
    _inherit = 'stock.picking'

    tot_qty = fields.Float(string='Total Quantity', compute='_compute_sum_quantity')

    @api.depends('move_ids_without_package')
    @api.depends('move_ids_without_package.product_uom_qty')
    def _compute_sum_quantity(self):
        for order in self:
            tot_qty = 0
            for line in order.move_ids_without_package:
                tot_qty += line.product_qty
            order.tot_qty = tot_qty
