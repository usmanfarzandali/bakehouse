# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class InventoryValuation(models.TransientModel):
    _name = "inventory.valuation.wizard"
    _description = "Inventory Valuation Wizard"

    date_from = fields.Date("From", required=True)
    date_to = fields.Date("To", required=True)
    categ_ids = fields.Many2many(comodel_name='product.category', string='Product Category')
    companies = fields.Many2many(comodel_name='res.company', string='Company')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    location_ids = fields.Many2many(comodel_name='stock.location', string='Location')
    inventory_type = fields.Selection([
        # ('detail', 'Detail Report'),
        # ('summary', 'Summary'),
        ('prod_stock', 'Product Stock'),
        ('location_wise', 'Location Wise'),
        # ('stock_wise', 'Stock Wise'),
        ('stock_summary', 'Stock Summary'),
        # ('stock_valuation', 'Stock Valuation'),
        ('valuation_summary', 'Valuation Summary'),
    ], string="Inventory Type", default='summary')

    file = fields.Binary('Download Report')
    name = fields.Char()

    @api.onchange ('categ_ids')
    def onchange_vendor(self):
        if self.categ_ids:
            return {'domain': {'product_id': [('categ_id', 'in', self.categ_ids.ids)]}}

    def generate_inventory_valuation_xlsx(self):
        return self.env.ref('inventory_valuation_xlsx.inventory_valuation_report').report_action(self)

    def generate_inventory_valuation_pdf(self):
        return self.env.ref('inventory_valuation_xlsx.inventory_valuation_report_pdf').report_action(self)

    def generate_inventory_summary_valuation_xlsx(self):
        return self.env.ref('inventory_valuation_xlsx.inventory_valuation_summary_report').report_action(self)

    def generate_inventory_summary_valuation_pdf(self):
        data = {'date_start': self.date_from, 'date_to': self.date_to,
                 }
        return self.env.ref('inventory_valuation_xlsx.inventory_valuation_summary_report_pdf').report_action(self,data={'wizard':data})

    def generate_product_stock_xlsx(self):
        return self.env.ref('inventory_valuation_xlsx.product_stock_report').report_action(self)

    def generate_product_stock_pdf(self):
        data = {'date_start': self.date_from, 'date_to': self.date_to,
                }
        return self.env.ref('inventory_valuation_xlsx.product_stock_report_pdf').report_action(self,data={'wizard':data})

    def generate_location_wise_xlsx(self):
        return self.env.ref('inventory_valuation_xlsx.inventory_valuation_location_report').report_action(self)

    def generate_location_wise_pdf(self):
        data = {'date_start': self.date_from, 'date_to': self.date_to,
                }
        return self.env.ref('inventory_valuation_xlsx.inventory_valuation_location_pdf').report_action(self,data ={'wizard':data})

    def generate_stock_wise_xlsx(self):
        return self.env.ref('inventory_valuation_xlsx.inventory_valuation_stock_report').report_action(self)

    def generate_stock_summary_xlsx(self):
        return self.env.ref('inventory_valuation_xlsx.inventory_stock_summary_report').report_action(self)

    def generate_stock_summary_pdf(self):
        data = {'date_start': self.date_from, 'date_to': self.date_to,
                }
        return self.env.ref('inventory_valuation_xlsx.inventory_stock_summary_report_pdf').report_action(self,data ={'wizard':data})

    def generate_stock_valuation_xlsx(self):
        return self.env.ref('inventory_valuation_xlsx.inv_value_detail_report').report_action(self)

    def generate_valuation_summary_xlsx(self):
        return self.env.ref('inventory_valuation_xlsx.inv_value_summary_report').report_action(self)

    def generate_valuation_summary_pdf(self):
        data = {'date_start': self.date_from, 'date_to': self.date_to,
                }
        return self.env.ref('inventory_valuation_xlsx.inv_value_summary_report_pdf').with_context(landscape=True).report_action(self,data ={'wizard':data})