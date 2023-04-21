from odoo import models, api, fields, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    lase_price = fields.Float(string="Last Purchase", readonly=1, store=True)

    @api.onchange('product_id')
    def _onchange_product_id_last_purchase(self):
        """it show the last purchase price"""
        for rec in self:
            last_purchase = self.env['purchase.order.line'].search([('product_id','=',rec.product_id.id),
                                                                    ('id','!=',rec._origin.id)], limit=1)
            if last_purchase:
                for record in last_purchase:
                    rec.lase_price = record.price_unit
