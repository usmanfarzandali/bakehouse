from num2words import num2words
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductVarientClass(models.AbstractModel):
    _name = 'report.product_barcode_space.report_variant_barcode'
    _description = 'Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['product.template'].browse(docids)

        # Getting current company
        company = self.env.company

        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'company': company,
            'docs': docs,
        }

######################################################

