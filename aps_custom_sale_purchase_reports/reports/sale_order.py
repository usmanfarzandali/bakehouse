from odoo import models, fields, api


class SaleOrderReport(models.AbstractModel):
    _name = 'report.aps_custom_sale_purchase_reports.sale_order_template'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['sale.order'].browse(docids)

        def date_format(date):
            if date:
                return date.strftime("%d-%b-%Y")

        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': docs,
            'date_format': date_format,
        }