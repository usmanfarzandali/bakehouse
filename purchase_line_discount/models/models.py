# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    #invisible field
    discount = fields.Float('Discount (%)', )
    discount_amount = fields.Monetary('Discount Amount', compute='_compute_amount_discount',digits='Discount')

    @api.onchange('discount')
    def _onchange_discount(self):
        for line in self.order_line:
            line.discount = self.discount

    @api.depends('order_line.unit_price_bfore_discount', 'order_line.discount')
    def _compute_amount_discount(self):
        for line in self:
            discount_amount = 0
            for line_order in line.order_line:
                discounted_price = line_order.product_qty*(line_order.unit_price_bfore_discount - line_order.price_unit)
                discount_amount += discounted_price
            line.update({
                'discount_amount': discount_amount
            })


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    discount = fields.Float('Discount (%)', digits='Discount')
    unit_price_bfore_discount = fields.Float('Unit Price', digits='Product Price')
    price_unit = fields.Float('Unit Price After Discount', store=True, compute='_compute_discounted_price',
                              digits='Product Price')

    @api.constrains('discount')
    def _check_unique_constraint(self):
        for rec in self:
            if rec.discount < 0 or rec.discount > 100:
                raise ValidationError('Discount must be in the range of 0-100%')

    @api.onchange('discount', 'unit_price_bfore_discount')
    def _onchange_price(self):
        # set auto-changing field
        if self.discount < 0 or self.discount > 100:
            return {
                'warning': {
                    'title': "Invalid Discount",
                    'message': "Discount must be in the range of 0-100%",
        }
            }

        self.price_unit = self.unit_price_bfore_discount * (1 - (self.discount or 0.0) / 100)

    @api.depends('discount', 'unit_price_bfore_discount')
    def _compute_discounted_price(self):
        for record in self:
            record.price_unit = record.unit_price_bfore_discount * (1 - record.discount / 100)

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        res = super(PurchaseOrderLine, self)._onchange_quantity()
        self.unit_price_bfore_discount = self.price_unit
        return res
