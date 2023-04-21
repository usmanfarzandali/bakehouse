from datetime import timedelta
from odoo import models


class SaleRegisterReport(models.AbstractModel):
    _name = 'report.aps_sale_register.sale_register_template'
    _description = "Sale Register XLSX Report"
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, report_detail, wizard_data):

        main_merge_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': '13',
             "font_color": 'black',
            "bg_color": '#F7DC6F',
            'font_name': 'Metropolis',
        })
        main_in_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': '13',
             "font_color": 'black',
            "bg_color": '#73C6B6',
            'font_name': 'Metropolis',
        })
        main_out_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': '13',
             "font_color": 'black',
            "bg_color": '#EB984E',
            'font_name': 'Metropolis',
        })
        format_data_header = workbook.add_format({
            "bold": 1,
            "border": 1,
            "align": 'center',
            "valign": 'vcenter',
            "font_color": 'black',
            "bg_color": '#F7DC6F',
            'font_size': '8',
            'font_name': 'Metropolis',
        })
        format_data_right = workbook.add_format({
            "border": 1,
            "align": 'right',
            "valign": 'vcenter',
            "font_color": 'black',
            'font_size': '8',
            'font_name': 'Metropolis',
            "num_format": "#,##0.00",
        })
        format_data_left = workbook.add_format({
            "border": 1,
            "align": 'left',
            "valign": 'vcenter',
            "font_color": 'black',
            'font_size': '8',
            'font_name': 'Metropolis',
            "num_format": "#,##0.00",
        })

        worksheet = workbook.add_worksheet('Sale Register Report')

        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:C', 15)
        worksheet.set_column('F:H', 15)
        worksheet.set_column('I:I', 35)
        worksheet.set_column('K:K', 35)
        worksheet.set_column('G:G', 15)

        worksheet.merge_range('A2:Q3', 'Sale Register Report', main_merge_format)

        row = 5
        col = 0

        domain = []
        if wizard_data.record_type == 'posted':
            domain += [('parent_state', '=', 'posted')]
        if wizard_data.date_from and wizard_data.date_to:
            domain += [('date', '>=', wizard_data.date_from), ('date', '<=', wizard_data.date_to)]
        if wizard_data.categ_ids:
            domain += [('product_id.categ_id', 'in', wizard_data.categ_ids.ids)]
        if wizard_data.partner_ids:
            domain += [('partner_id', 'in', wizard_data.partner_ids.ids)]
        if wizard_data.product_ids:
            domain += [('product_id', 'in', wizard_data.product_ids.ids)]
        if wizard_data.order_number:
            domain += [('move_id.invoice_origin', '=', wizard_data.order_number)]

        invoice_records = self.env['account.move.line'].search(domain)

        worksheet.merge_range(row, col, row, col+1, 'Date From', format_data_header)
        worksheet.write_string(row, col+2, str(wizard_data.date_from), format_data_left)

        row += 1
        worksheet.merge_range(row, col, row, col+1, 'Date To', format_data_header)
        worksheet.write_string(row, col+2, str(wizard_data.date_to), format_data_left)

        row += 2

        worksheet.write_string(row, col, 'Sr. No', format_data_header)
        worksheet.write_string(row, col + 1, 'Date', format_data_header)
        worksheet.write_string(row, col + 2, 'Invoice No', format_data_header)
        worksheet.write_string(row, col + 3, 'OGP', format_data_header)
        worksheet.write_string(row, col + 4, 'SO #', format_data_header)
        worksheet.write_string(row, col + 5, 'Partner', format_data_header)
        worksheet.write_string(row, col + 6, 'sales Person', format_data_header)
        worksheet.write_string(row, col + 7, 'NTN', format_data_header)
        worksheet.write_string(row, col + 8, 'Product', format_data_header)
        worksheet.write_string(row, col + 9, 'Category', format_data_header)
        worksheet.write_string(row, col + 10, 'Label', format_data_header)
        worksheet.write_string(row, col + 11, 'Qty', format_data_header)
        worksheet.write_string(row, col + 12, 'Price', format_data_header)
        worksheet.write_string(row, col + 13, 'Discount', format_data_header)
        worksheet.write_string(row, col + 14, 'Tax', format_data_header)
        worksheet.write_string(row, col + 15, 'Subtotal', format_data_header)
        worksheet.write_string(row, col + 16, 'Total', format_data_header)
        row += 1
        serial = 1

        for record in invoice_records:
            if record.move_id.invoice_origin and record.move_id.move_type in ['out_invoice', 'out_refund']:
                if record.product_id:
                    taxes = 0.0
                    if record.tax_ids:
                        for tax in record.tax_ids:
                            taxes += record.price_subtotal/100 * tax.amount
                    total = record.price_subtotal + taxes
                    worksheet.write_string(row, col, str(serial), format_data_left)
                    worksheet.write_string(row, col + 1, str(record.move_id.date or ''), format_data_left)
                    worksheet.write_string(row, col + 2, str(record.move_id.name or ''), format_data_left)
                    worksheet.write_string(row, col + 3, str(record.move_id.narration or ''), format_data_left)
                    worksheet.write_string(row, col + 4, str(record.move_id.invoice_origin or ''), format_data_left)
                    worksheet.write_string(row, col + 5, str(record.partner_id.name or ''), format_data_left)
                    worksheet.write_string(row, col + 6, str(record.partner_id.user_id.name or ''), format_data_left)
                    worksheet.write_string(row, col + 7, str(record.partner_id.vat or ''), format_data_left)
                    worksheet.write_string(row, col + 8, str(record.product_id.name or ''), format_data_left)
                    worksheet.write_string(row, col + 9, str(record.product_id.categ_id.name or ''), format_data_left)
                    worksheet.write_string(row, col + 10, str(record.name or ''), format_data_left)
                    worksheet.write_number(row, col + 11, record.quantity, format_data_right)
                    worksheet.write_number(row, col + 12, record.price_unit, format_data_right)
                    worksheet.write_number(row, col + 13, record.discount, format_data_right)
                    worksheet.write_number(row, col + 14, taxes, format_data_right)
                    worksheet.write_number(row, col + 15, record.price_subtotal, format_data_right)
                    if record.move_id.reversed_entry_id:
                        worksheet.write_number(row, col + 16, (total * -1), format_data_right)
                    else:
                        worksheet.write_number(row, col + 16, total, format_data_right)
                    serial += 1
                    row += 1


class SaleRegisterDetailPdf(models.AbstractModel):
    _name = 'report.aps_sale_register.sale_register_detail_report_pdf'

    def _get_report_values(self, docids, data=None):
        ids = self._context.get('active_ids')

        wizard_data = self.env['sale.register.wizard'].browse(self.env.context.get('active_ids'))

        domain = []
        if wizard_data.record_type == 'posted':
            domain += [('parent_state', '=', 'posted')]
        if wizard_data.date_from and wizard_data.date_to:
            domain += [('date', '>=', wizard_data.date_from), ('date', '<=', wizard_data.date_to)]
        if wizard_data.categ_ids:
            domain += [('product_id.categ_id', 'in', wizard_data.categ_ids.ids)]
        if wizard_data.partner_ids:
            domain += [('partner_id', 'in', wizard_data.partner_ids.ids)]
        if wizard_data.order_number:
            domain += [('move_id.invoice_origin', '=', wizard_data.order_number)]

        invoice_records = self.env['account.move.line'].search(domain)

        so_list = []
        data_list = []
        for record in invoice_records:
            if record.move_id.invoice_origin and record.move_id.move_type in ['out_invoice', 'out_refund']:
                if record.product_id:
                    taxes = 0.0
                    if record.tax_ids:
                        for tax in record.tax_ids:
                            taxes += record.price_subtotal / 100 * tax.amount
                    total = record.price_subtotal + taxes
                    so_list.append(record.move_id.id)
                    data_list.append({
                        'date': record.move_id.date or '',
                        'invoice_no': record.move_id.name or '',
                        'ogp': record.move_id.narration or '',
                        'so': record.move_id.invoice_origin or '',
                        'partner': record.partner_id.name or '',
                        'saleperson': record.partner_id.user_id.name or '',
                        'ntn': record.partner_id.vat or '',
                        'product': record.product_id.name or '',
                        'category': record.product_id.categ_id.name or '',
                        'label': record.name or '',
                        'qty': record.quantity or '0.00',
                        'price': record.price_unit or '0.00',
                        'discount': record.discount or '0.00',
                        'tax': record.move_id.amount_tax or '0.00',
                        'subtotal': record.price_subtotal or '0.00',
                        'total': total or '0.00',


                    })



        return {
            'doc_ids': docids,
            'doc_model': 'partner.ledger.wizard',
            'data': data_list,
            'wizard_data': wizard_data,
        }
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
