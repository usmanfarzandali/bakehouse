from num2words import num2words
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EffectiveDateNotice(models.AbstractModel):
    _name = 'report.product_barcode_space.report_product_t_barcode'
    _description = 'Report'


    @api.model
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

