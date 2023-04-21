from odoo import models, fields, api


class PurchaseOrderReport(models.AbstractModel):
    _name = 'report.aps_custom_sale_purchase_reports.purchase_order_template'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['purchase.order'].browse(docids)

        def date_format(date):
            if date:
                return date.strftime("%d-%b-%Y")

        return {
            'doc_ids': docids,
            'doc_model': 'purchase.order',
            'docs': docs,
            'date_format': date_format,
        }