from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    lase_price = fields.Float(string="Last Sale", readonly=1, store=True)

    @api.onchange('product_id')
    def _onchange_product_id_last_sale(self):
        """it show the last sale price"""
        for rec in self:
            last_sale = self.env['sale.order.line'].search([('product_id','=',rec.product_id.id),
                                                                    ('id','!=',rec._origin.id)], limit=1)
            if last_sale:
                for record in last_sale:
                    rec.lase_price = record.price_unit
