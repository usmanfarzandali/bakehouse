from datetime import timedelta
from odoo import models
from datetime import datetime, time
class SupplierLedgerReportPdf(models.AbstractModel):
    _name = 'report.aps_accounting_report.report_student_id_card'

    def _get_report_values(self, docids, data=None):
        global DDate
        data = self.env['partner.ledger.wizard'].browse(self.env.context.get('active_ids'))

        wizard_data = self.env['partner.ledger.wizard'].browse(self.env.context.get('active_ids'))
        domain = [('parent_state', '=', 'posted')]
        if wizard_data.date_from and wizard_data.date_to:
            domain += [('date', '>=', wizard_data.date_from), ('date', '<=', wizard_data.date_to)]
        if wizard_data.partner_ids:
            domain += [('partner_id', 'in', wizard_data.partner_ids.ids)]
        if wizard_data.partner_type == 'customer':
            domain += [('partner_id.customer_rank', '>=', 1)]
        if wizard_data.partner_type == 'vendor':
            domain += [('partner_id.supplier_rank', '>=', 1)]
        if wizard_data.companies:
            domain += [('company_id', 'in', wizard_data.companies.ids)]

        invoice_records = self.env['account.move.line'].search(domain)
        partner_ident = []
        data_list = []
        for invoices in invoice_records:
            if invoices.partner_id.id not in partner_ident:
                partner_ident.append(invoices.partner_id.id)
                opening_data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                                     ('partner_id', '=', invoices.partner_id.id),
                                                                     ('date', '<', wizard_data.date_from)])
                opening = 0.0
                for rec in opening_data:
                    if rec.account_id.id in [rec.partner_id.property_account_payable_id.id,
                                             rec.partner_id.property_account_receivable_id.id]:
                        opening += rec.debit - rec.credit
                partner_data = invoice_records.search([('parent_state', '=', 'posted'),
                                                       ('partner_id', '=', invoices.partner_id.id),
                                                       ('date', '>=', wizard_data.date_from),
                                                       ('date', '<=', wizard_data.date_to)], order="date asc")
                debit = 0.0
                credit = 0.0

                if partner_data:
                    closing = 0.0
                    for record in partner_data:
                        if record.account_id.id in [record.partner_id.property_account_payable_id.id,
                                                    record.partner_id.property_account_receivable_id.id]:
                            debit += record.debit
                            credit += record.credit
                            closing = (debit - credit) + opening
                            data_list.append({
                                    'partner': invoices.partner_id.name or '',
                                    'date': record.date or '',
                                    'invoice_no': record.account_id.display_name or '',
                                    'ogp': record.move_id.display_name or '',
                                    'so': record.name or '',
                                    'opening': opening or '',
                                    'debit': record.debit or '',
                                    'credit': record.credit or '',
                                    'closing': closing or '',
                                  })

        docs = self.env['partner.ledger.wizard'].browse(docids)

        invoice_records_multi = self.env['account.move'].search([])
        invoice_records = invoice_records_multi[0]
        now = datetime.now()
        current_time ="{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        Uuser = self.env.user.name
        # comp = wizard_data.companies.name

        return {
            'doc_ids': docids,
            'doc_model': 'partner.ledger.wizard',
            'data': data_list,
            'wizard_data': wizard_data,
            'DDate': current_time,
            'Uuser': Uuser,
            # 'comp': comp,

        }




# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class SupplierMovementReport(models.AbstractModel):
    _name = 'report.aps_accounting_report.partner_ledger_template'
    _description = "Partner Ledger XLSX Report"
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

        worksheet = workbook.add_worksheet('Partner Ledger Report')

        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:E', 35)
        worksheet.set_column('F:H', 12)

        worksheet.merge_range('A2:H3', 'Partner Ledger Report', main_merge_format)

        row = 5
        col = 0

        domain = [('parent_state', '=', 'posted')]
        if wizard_data.date_from and wizard_data.date_to:
            domain += [('date', '>=', wizard_data.date_from), ('date', '<=', wizard_data.date_to)]
        if wizard_data.partner_ids:
            domain += [('partner_id', 'in', wizard_data.partner_ids.ids)]
        if wizard_data.partner_type == 'customer':
            domain += [('partner_id.customer_rank', '>=', 1)]
        if wizard_data.partner_type == 'vendor':
            domain += [('partner_id.supplier_rank', '>=', 1)]
        if wizard_data.companies:
            domain += [('company_id', 'in', wizard_data.companies.ids)]

        invoice_records = self.env['account.move.line'].search(domain)


        worksheet.merge_range(row, col, row, col + 1, 'User', format_data_header)
        current_user = self.env.user.name
        worksheet.write_string(row, col + 2, str(current_user), format_data_left)

        row += 1
        worksheet.merge_range(row, col, row, col+1, 'Date From', format_data_header)
        worksheet.write_string(row, col+2, str(wizard_data.date_from), format_data_left)

        row += 1
        worksheet.merge_range(row, col, row, col+1, 'Date To', format_data_header)
        worksheet.write_string(row, col+2, str(wizard_data.date_to), format_data_left)
        worksheet.write_string(row, col + 5,  'Company ', format_data_header)
        worksheet.merge_range(row, col + 6, row, col + 7, str(wizard_data.companies.mapped('name')), format_data_left)

        row += 3

        worksheet.write_string(row, col, 'Sr. No', format_data_header)
        worksheet.write_string(row, col + 1, 'Date', format_data_header)
        worksheet.write_string(row, col + 2, 'Account', format_data_header)
        worksheet.write_string(row, col + 3, 'Reference', format_data_header)
        worksheet.write_string(row, col + 4, 'Label', format_data_header)
        worksheet.write_string(row, col + 5, 'Debit', format_data_header)
        worksheet.write_string(row, col + 6, 'Credit', format_data_header)
        worksheet.write_string(row, col + 7, 'Balance', format_data_header)
        row += 1
        serial = 1

        partner_ident = []
        for invoices in invoice_records:
            if invoices.partner_id.id not in partner_ident:
                partner_ident.append(invoices.partner_id.id)
                opening_data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                       ('partner_id', '=', invoices.partner_id.id),
                                                       ('date', '<', wizard_data.date_from)])
                opening = 0.0
                for rec in opening_data:
                    if rec.account_id.id in [rec.partner_id.property_account_payable_id.id, rec.partner_id.property_account_receivable_id.id]:
                        opening += rec.debit - rec.credit
                partner_data = invoice_records.search([('parent_state', '=', 'posted'),
                                                       ('partner_id', '=', invoices.partner_id.id),
                                                       ('date', '>=', wizard_data.date_from),
                                                       ('date', '<=', wizard_data.date_to)], order="date asc")
                debit = 0.0
                credit = 0.0
                if partner_data:
                    row += 2
                    worksheet.merge_range(row, col, row, col + 2, invoices.partner_id.name, format_data_header)
                    worksheet.merge_range(row, col + 5, row, col + 6, "Opening", format_data_header)
                    worksheet.write_number(row, col + 7, opening, format_data_right)
                    row += 1
                    closing = 0.0
                    for record in partner_data:
                        if record.account_id.id in [record.partner_id.property_account_payable_id.id, record.partner_id.property_account_receivable_id.id]:
                            debit += record.debit
                            credit += record.credit
                            closing = (debit - credit) + opening
                            worksheet.write_string(row, col, str(serial), format_data_left)
                            worksheet.write_string(row, col + 1, str(record.date or ''), format_data_left)
                            worksheet.write_string(row, col + 2, str(record.account_id.display_name or ''), format_data_right)
                            worksheet.write_string(row, col + 3, str(record.move_id.display_name or ''), format_data_right)
                            worksheet.write_string(row, col + 4, str(record.name or ''), format_data_right)
                            worksheet.write_number(row, col + 5, record.debit, format_data_right)
                            worksheet.write_number(row, col + 6, record.credit, format_data_right)
                            worksheet.write_number(row, col + 7, closing, format_data_right)
                            serial += 1
                            row += 1
                    worksheet.merge_range(row, col + 5, row, col + 6, "Closing", format_data_header)
                    worksheet.write_number(row, col + 7, closing, format_data_right)
                    row += 1

        now = datetime.now()
        current_time = "{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        row += 1
        worksheet.merge_range(row, col, row, col + 1, 'Print Date', format_data_header)
        worksheet.write_string(row, col + 2, str(current_time), format_data_left)