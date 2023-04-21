# -*- coding: utf-8 -*-


import logging
from odoo import api, fields, models, tools, _
import odoo.addons.decimal_precision as dp
from itertools import groupby
_logger = logging.getLogger(__name__)

class pos_multi_barcode_opt(models.Model):
    _name = 'pos.multi.barcode.options'
    _rec_name = 'package_name'

    package_name =  fields.Char('Pkg Name',required=True)
    name = fields.Char('Barcode',required=True)
    qty = fields.Float("Quantity")
    price = fields.Float("Price")
    unit = fields.Many2one("uom.uom",string="Unit")
    product_id = fields.Many2one("product.product",string="Product")


    @api.onchange('unit')
    def unit_id_change(self):
        domain = {'unit': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        return {'domain': domain}


class product_product(models.Model):
    _inherit = 'product.product'

    pos_multi_barcode_option = fields.One2many('pos.multi.barcode.options','product_id',string='Barcodes')

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    product_uom = fields.Many2one('uom.uom','Unit of measure')



class StockPicking(models.Model):
    _inherit='stock.picking'

    def _prepare_stock_move_vals(self, first_line, order_lines):
        res = super(StockPicking, self)._prepare_stock_move_vals(first_line, order_lines)
        res['product_uom'] = first_line.product_uom.id or first_line.product_id.uom_id.id,
        return res

    def _create_move_from_pos_order_lines(self, lines):
        self.ensure_one()
        lines_by_product = groupby(sorted(lines, key=lambda l: l.product_id.id), key=lambda l: (l.product_id.id,l.product_uom.id))
        for product, lines in lines_by_product:
            order_lines = self.env['pos.order.line'].concat(*lines)
            first_line = order_lines[0]
            current_move = self.env['stock.move'].create(
                self._prepare_stock_move_vals(first_line, order_lines)
            )
            if first_line.product_id.tracking != 'none' and (self.picking_type_id.use_existing_lots or self.picking_type_id.use_create_lots):
                for line in order_lines:
                    sum_of_lots = 0
                    for lot in line.pack_lot_ids.filtered(lambda l: l.lot_name):
                        if line.product_id.tracking == 'serial':
                            qty = 1
                        else:
                            qty = abs(line.qty)
                        ml_vals = current_move._prepare_move_line_vals()
                        ml_vals.update({'qty_done':qty})
                        if self.picking_type_id.use_existing_lots:
                            existing_lot = self.env['stock.production.lot'].search([
                                ('company_id', '=', self.company_id.id),
                                ('product_id', '=', line.product_id.id),
                                ('name', '=', lot.lot_name)
                            ])
                            if not existing_lot and self.picking_type_id.use_create_lots:
                                existing_lot = self.env['stock.production.lot'].create({
                                    'company_id': self.company_id.id,
                                    'product_id': line.product_id.id,
                                    'name': lot.lot_name,
                                })
                            ml_vals.update({
                                'lot_id': existing_lot.id,
                            })
                        else:
                            ml_vals.update({
                                'lot_name': lot.lot_name,
                            })
                        self.env['stock.move.line'].create(ml_vals)
                        sum_of_lots += qty
                    if abs(line.qty) != sum_of_lots:
                        difference_qty = abs(line.qty) - sum_of_lots
                        ml_vals = current_move._prepare_move_line_vals()
                        if line.product_id.tracking == 'serial':
                            ml_vals.update({'qty_done': 1})
                            for i in range(int(difference_qty)):
                                self.env['stock.move.line'].create(ml_vals)
                        else:
                            ml_vals.update({'qty_done': difference_qty})
                            self.env['stock.move.line'].create(ml_vals)
            else:
                current_move.quantity_done = abs(sum(order_lines.mapped('qty')))