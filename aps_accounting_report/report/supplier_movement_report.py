from datetime import timedelta
from odoo import models
from datetime import datetime, time

class SupplierMovementReportPdf(models.AbstractModel):
    _name = 'report.aps_accounting_report.report_supplier_id_card'

    def _get_report_values(self, docids, data=None):
        data_list = []
        global partner_main_list
        data = self.env['supplier.movement.wizard'].browse(self.env.context.get('active_ids'))

        wizard_data = self.env['supplier.movement.wizard'].browse(self.env.context.get('active_ids'))
        domain = [('state', '=', 'posted')]
        if wizard_data.date_from and wizard_data.date_to:
            domain += [('invoice_date', '>=', wizard_data.date_from), ('invoice_date', '<=', wizard_data.date_to)]
        if wizard_data.partner_ids:
            domain += [('partner_id', 'in', wizard_data.partner_ids.ids)]
        if wizard_data.partner_type == 'customer':
            domain += [('partner_id.customer_rank', '>=', 1)]
        if wizard_data.partner_type == 'vendor':
            domain += [('partner_id.supplier_rank', '>=', 1)]
        if wizard_data.companies:
            domain += [('company_id', 'in', wizard_data.companies.ids)]

        invoice_records = self.env['account.move'].search(domain)
        for invoices in invoice_records:
            partner_main_list = []
            partner_ident = []
            for invoices in invoice_records:
                sale = 0.0
                purchase = 0.0
                pur_ret = 0.0
                sale_ret = 0.0
                dr_note = 0.0
                cr_note = 0.0
                opening = 0.0
                payment = 0.0
                collection = 0.0
                if invoices.partner_id.id not in partner_ident:
                    partner_ident.append(invoices.partner_id.id)
                    if not opening:
                        opening_data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                                             (
                                                                                 'partner_id', '=',
                                                                                 invoices.partner_id.id),
                                                                             ('date', '<', wizard_data.date_from)])
                        for rec in opening_data:
                            if rec.account_id.id in [rec.partner_id.property_account_payable_id.id,
                                                     rec.partner_id.property_account_receivable_id.id]:
                                opening += rec.debit - rec.credit
                    partner_data = self.env['account.move'].search([('state', '=', 'posted'),
                                                                    ('partner_id', '=', invoices.partner_id.id),
                                                                    ('date', '>=', wizard_data.date_from),
                                                                    ('date', '<=', wizard_data.date_to)],
                                                                   order="date asc")
                    if partner_data:
                        print(11111111111111111111111111111111111111111111111111111111111111, partner_data)
                        for sub_rec in partner_data:
                            if sub_rec.move_type == 'out_invoice':
                                sale += sub_rec.amount_total
                            if sub_rec.move_type == 'in_invoice':
                                purchase += sub_rec.amount_total
                            if sub_rec.move_type == 'out_refund':
                                if not sub_rec.reversed_entry_id:
                                    sale_ret += sub_rec.amount_total
                                else:
                                    dr_note += sub_rec.amount_total
                            if sub_rec.move_type == 'in_refund':
                                if not sub_rec.reversed_entry_id:
                                    pur_ret += sub_rec.amount_total
                                else:
                                    cr_note += sub_rec.amount_total
                    payments_rec = self.env['account.payment'].search([('partner_id', '=', invoices.partner_id.id),
                                                                       ('date', '>=', wizard_data.date_from),
                                                                       ('date', '<=', wizard_data.date_to)])
                    for pay in payments_rec:
                        if pay.payment_type == 'outbound':
                            payment += pay.amount
                        if pay.payment_type == 'inbound':
                            collection += pay.amount
                    ven_closing = abs(opening) + abs(purchase) - abs(pur_ret) + abs(cr_note) - abs(dr_note) - abs(
                        payment)
                    cust_closing = abs(opening) + abs(sale) - abs(sale_ret) + abs(dr_note) - abs(cr_note) - abs(
                        collection)
                    closing = opening + (cust_closing - ven_closing)
                    part_lis = [invoices.partner_id.name, opening, sale, sale_ret, dr_note, collection, purchase,
                                pur_ret,
                                cr_note, payment, closing, cust_closing, ven_closing]
                    partner_main_list.append(part_lis)

            data_list = []
            for rec_data in partner_main_list:
                data_list.append({
                   'partner_name': rec_data[0],
                   'opening_balance': rec_data[1],
                   'sale': rec_data[2],
                   's_return': rec_data[3],
                   'debit_note': rec_data[4],
                   'collection': rec_data[5],
                   'purchase': rec_data[6],
                   'p_return': rec_data[7],
                   'credit_note': rec_data[8],
                   'payment': rec_data[9],
                   'closing_balance': rec_data[10],
            })

        docs = self.env['partner.ledger.wizard'].browse(docids)

        invoice_records_multi = self.env['account.move'].search([])
        invoice_records = invoice_records_multi[0]

        now = datetime.now()
        current_time = "{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        Uuser = self.env.user.name
        # for com in wizard_data.companies:
        #     comp = com[0]

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
    _name = 'report.aps_accounting_report.supplier_movement_template'
    _description = "Supplier Movement XLSX Report"
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

        worksheet = workbook.add_worksheet('Partner Movement Report')

        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 35)
        worksheet.set_column('C:L', 12)

        if wizard_data.partner_type == 'customer' or wizard_data.partner_type == 'vendor':
            worksheet.merge_range('A2:H3', 'Partner Movement Report', main_merge_format)
        else:
            worksheet.merge_range('A2:L3', 'Partner Movement Report', main_merge_format)

        row = 5
        col = 0

        domain = [('state', '=', 'posted')]
        if wizard_data.date_from and wizard_data.date_to:
            domain += [('invoice_date', '>=', wizard_data.date_from), ('invoice_date', '<=', wizard_data.date_to)]
        if wizard_data.partner_ids:
            domain += [('partner_id', 'in', wizard_data.partner_ids.ids)]
        if wizard_data.partner_type == 'customer':
            domain += [('partner_id.customer_rank', '>=', 1)]
        if wizard_data.partner_type == 'vendor':
            domain += [('partner_id.supplier_rank', '>=', 1)]
        if wizard_data.companies:
            domain += [('company_id', 'in', wizard_data.companies.ids)]

        invoice_records = self.env['account.move'].search(domain)


        worksheet.merge_range(row, col, row, col + 1, 'User', format_data_header)
        current_user = self.env.user.name
        worksheet.write_string(row, col + 2, str(current_user), format_data_left)

        row += 1
        worksheet.merge_range(row, col, row, col + 1, 'Date From', format_data_header)
        worksheet.write_string(row, col + 2, str(wizard_data.date_from), format_data_left)
        worksheet.merge_range(row, col + 5, row, col + 6, 'Company', format_data_header)

        worksheet.merge_range(row, col + 7, row, col + 8, str(wizard_data.companies.mapped('name')), format_data_left)

        if wizard_data.partner_type == 'customer' or wizard_data.partner_type == 'vendor':
            worksheet.merge_range(row, col + 5, row, col + 6, 'Partner Type', format_data_header)
            worksheet.write_string(row, col + 7, str(dict(wizard_data._fields['partner_type'].selection).get(
                wizard_data.partner_type)), format_data_left)
        else:
            worksheet.merge_range(row, col + 9, row, col + 10, 'Partner Type', format_data_header)
            worksheet.write_string(row, col + 11, str(dict(wizard_data._fields['partner_type'].selection).get(
                wizard_data.partner_type)), format_data_left)
        row += 1
        worksheet.merge_range(row, col, row, col + 1, 'Date To', format_data_header)
        worksheet.write_string(row, col + 2, str(wizard_data.date_to), format_data_left)

        row += 3

        partner_main_list = []
        partner_ident = []
        for invoices in invoice_records:
            sale = 0.0
            purchase = 0.0
            pur_ret = 0.0
            sale_ret = 0.0
            dr_note = 0.0
            cr_note = 0.0
            opening = 0.0
            payment = 0.0
            collection = 0.0
            if invoices.partner_id.id not in partner_ident:
                partner_ident.append(invoices.partner_id.id)
                if not opening:
                    opening_data = self.env['account.move.line'].search([('parent_state', '=', 'posted'),
                                                                         ('partner_id', '=', invoices.partner_id.id),
                                                                         ('date', '<', wizard_data.date_from)])
                    for rec in opening_data:
                        if rec.account_id.id in [rec.partner_id.property_account_payable_id.id,
                                                 rec.partner_id.property_account_receivable_id.id]:
                            opening += rec.debit - rec.credit
                partner_data = self.env['account.move'].search([('state', '=', 'posted'),
                                                                ('partner_id', '=', invoices.partner_id.id),
                                                                ('date', '>=', wizard_data.date_from),
                                                                ('date', '<=', wizard_data.date_to)], order="date asc")
                if partner_data:
                    print(11111111111111111111111111111111111111111111111111111111111111, partner_data)
                    for sub_rec in partner_data:
                        if sub_rec.move_type == 'out_invoice':
                            sale += sub_rec.amount_total
                        if sub_rec.move_type == 'in_invoice':
                            purchase += sub_rec.amount_total
                        if sub_rec.move_type == 'out_refund':
                            if not sub_rec.reversed_entry_id:
                                sale_ret += sub_rec.amount_total
                            else:
                                dr_note += sub_rec.amount_total
                        if sub_rec.move_type == 'in_refund':
                            if not sub_rec.reversed_entry_id:
                                pur_ret += sub_rec.amount_total
                            else:
                                cr_note += sub_rec.amount_total
                payments_rec = self.env['account.payment'].search([('partner_id', '=', invoices.partner_id.id),
                                                                   ('date', '>=', wizard_data.date_from),
                                                                   ('date', '<=', wizard_data.date_to)])
                for pay in payments_rec:
                    if pay.payment_type == 'outbound':
                        payment += pay.amount
                    if pay.payment_type == 'inbound':
                        collection += pay.amount
                ven_closing = abs(opening) + abs(purchase) - abs(pur_ret) + abs(cr_note) - abs(dr_note) - abs(payment)
                cust_closing = abs(opening) + abs(sale) - abs(sale_ret) + abs(dr_note) - abs(cr_note) - abs(collection)
                closing = opening + (cust_closing - ven_closing)
                part_lis = [invoices.partner_id.name, opening, sale, sale_ret, dr_note, collection, purchase, pur_ret,
                            cr_note, payment, closing, cust_closing, ven_closing]
                partner_main_list.append(part_lis)

        if wizard_data.partner_type == 'customer':
            worksheet.write_string(row, col, 'Sr. No', format_data_header)
            worksheet.write_string(row, col + 1, 'Partner Name', format_data_header)
            worksheet.write_string(row, col + 2, 'Opening Balance', format_data_header)
            worksheet.write_string(row, col + 3, 'Sale', format_data_header)
            worksheet.write_string(row, col + 4, 'S.Return', format_data_header)
            worksheet.write_string(row, col + 5, 'Debit Note', format_data_header)
            worksheet.write_string(row, col + 6, 'Collection', format_data_header)
            worksheet.write_string(row, col + 7, 'Closing Balance', format_data_header)
            row += 1
            serial = 1

            if partner_main_list:
                for invoice in partner_main_list:
                    worksheet.write_string(row, col, str(serial), format_data_left)
                    worksheet.write_string(row, col + 1, invoice[0] or '', format_data_left)
                    worksheet.write_number(row, col + 2, invoice[1], format_data_right)
                    worksheet.write_number(row, col + 3, invoice[2], format_data_right)
                    worksheet.write_number(row, col + 4, invoice[3], format_data_right)
                    worksheet.write_number(row, col + 5, invoice[4], format_data_right)
                    worksheet.write_number(row, col + 6, invoice[5], format_data_right)
                    worksheet.write_number(row, col + 7, invoice[11], format_data_right)
                    serial += 1
                    row += 1

        elif wizard_data.partner_type == 'vendor':
            worksheet.write_string(row, col, 'Sr. No', format_data_header)
            worksheet.write_string(row, col + 1, 'Partner Name', format_data_header)
            worksheet.write_string(row, col + 2, 'Opening Balance', format_data_header)
            worksheet.write_string(row, col + 3, 'Purchase', format_data_header)
            worksheet.write_string(row, col + 4, 'P.Return', format_data_header)
            worksheet.write_string(row, col + 5, 'Credit Note', format_data_header)
            worksheet.write_string(row, col + 6, 'Payment', format_data_header)
            worksheet.write_string(row, col + 7, 'Closing Balance', format_data_header)
            row += 1
            serial = 1

            if partner_main_list:
                for invoice in partner_main_list:
                    worksheet.write_string(row, col, str(serial), format_data_left)
                    worksheet.write_string(row, col + 1, invoice[0] or '', format_data_left)
                    worksheet.write_number(row, col + 2, invoice[1], format_data_right)
                    worksheet.write_number(row, col + 3, invoice[6], format_data_right)
                    worksheet.write_number(row, col + 4, invoice[7], format_data_right)
                    worksheet.write_number(row, col + 5, invoice[8], format_data_right)
                    worksheet.write_number(row, col + 6, invoice[9], format_data_right)
                    worksheet.write_number(row, col + 7, invoice[12], format_data_right)
                    serial += 1
                    row += 1
        else:
            worksheet.write_string(row, col, 'Sr. No', format_data_header)
            worksheet.write_string(row, col + 1, 'Partner Name', format_data_header)
            worksheet.write_string(row, col + 2, 'Opening Balance', format_data_header)
            worksheet.write_string(row, col + 3, 'Sale', format_data_header)
            worksheet.write_string(row, col + 4, 'S.Return', format_data_header)
            worksheet.write_string(row, col + 5, 'Debit Note', format_data_header)
            worksheet.write_string(row, col + 6, 'Collection', format_data_header)
            worksheet.write_string(row, col + 7, 'Purchase', format_data_header)
            worksheet.write_string(row, col + 8, 'P.Return', format_data_header)
            worksheet.write_string(row, col + 9, 'Credit Note', format_data_header)
            worksheet.write_string(row, col + 10, 'Payment', format_data_header)
            worksheet.write_string(row, col + 11, 'Closing Balance', format_data_header)
            row += 1
            serial = 1

            if partner_main_list:
                for invoice in partner_main_list:
                    worksheet.write_string(row, col, str(serial), format_data_left)
                    worksheet.write_string(row, col + 1, invoice[0] or '', format_data_left)
                    worksheet.write_number(row, col + 2, invoice[1], format_data_right)
                    worksheet.write_number(row, col + 3, invoice[2], format_data_right)
                    worksheet.write_number(row, col + 4, invoice[3], format_data_right)
                    worksheet.write_number(row, col + 5, invoice[4], format_data_right)
                    worksheet.write_number(row, col + 6, invoice[5], format_data_right)
                    worksheet.write_number(row, col + 7, invoice[6], format_data_right)
                    worksheet.write_number(row, col + 8, invoice[7], format_data_right)
                    worksheet.write_number(row, col + 9, invoice[8], format_data_right)
                    worksheet.write_number(row, col + 10, invoice[9], format_data_right)
                    worksheet.write_number(row, col + 11, invoice[10], format_data_right)
                    serial += 1
                    row += 1

        # worksheet.merge_range(row, col, row, col + 1, 'Total', format_data_header)
        # worksheet.write_string(row, col + 3, sum('opening'), format_data_left)
        # worksheet.write_string(row, col + 4, str('k'), format_data_left)
        # worksheet.write_string(row, col + 5, str('k'), format_data_left)
        # worksheet.write_string(row, col + 6, str('k'), format_data_left)
        # worksheet.write_string(row, col + 7, str('k'), format_data_left)
        # worksheet.write_string(row, col + 8, str('k'), format_data_left)
        # worksheet.write_string(row, col + 9, str('k'), format_data_left)
        # worksheet.write_string(row, col + 10, str('k'), format_data_left)
        # worksheet.write_string(row, col + 11, str(''), format_data_left)

        now = datetime.now()
        current_time = "{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        row += 1
        worksheet.merge_range(row, col, row, col + 1, 'Print Date', format_data_header)
        worksheet.write_string(row, col + 2, str(current_time), format_data_left)