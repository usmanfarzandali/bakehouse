from odoo import models, fields, api, _


class ProductProductVarientClass(models.AbstractModel):
    _name = 'report.product_barcode_space.report_product_price_barcode'
    _description = 'Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['product.product'].browse(docids)

        # Getting current company
        company = self.env.company

        return {
            'doc_ids': docids,
            'doc_model': 'product.product',
            'company': company,
            'docs': docs,
        }

