from datetime import timedelta
from odoo import models
from datetime import datetime, time


class CODPaymentXlsx(models.AbstractModel):
    _name = 'report.inventory_valuation_xlsx.inv_valuation_stock_template'
    _description = "Inventory Valuation XLSX Report"
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

        worksheet = workbook.add_worksheet('Inventory OPSI Report')

        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 12)
        worksheet.set_column('C:D', 13)
        worksheet.set_column('E:H', 10)
        worksheet.set_column('I:I', 12)
        worksheet.set_column('J:L', 10)
        worksheet.set_column('M:M', 12)

        worksheet.merge_range('A2:M3', 'Inventory OPSI Report', main_merge_format)

        row = 5
        col = 0

        domain = [('state', '=', 'done')]
        if wizard_data.date_from and wizard_data.date_to:
            domain += [('date', '>=', wizard_data.date_from), ('date', '<=', wizard_data.date_to)]
        if wizard_data.categ_ids:
            domain += [('product_id.categ_id', 'in', wizard_data.categ_ids.ids)]
        if wizard_data.product_id:
            domain += [('product_id', '=', wizard_data.product_id.id)]
        if wizard_data.companies:
            domain += [('company_id', 'in', wizard_data.companies.ids)]


        move_lines_records = self.env['stock.move.line'].search(domain)
        move_lines_record = sorted(move_lines_records, key=lambda move: move.product_id.id)

        worksheet.write_string(row, col, 'User', format_data_header)
        current_user = self.env.user.name
        worksheet.write_string(row, col + 1, str(current_user), format_data_left)
        row += 1
        worksheet.write_string(row, col, 'Date From', format_data_header)
        worksheet.write_string(row, col+1, str(wizard_data.date_from), format_data_left)
        row += 1
        worksheet.write_string(row, col, 'Date To', format_data_header)
        worksheet.write_string(row, col+1, str(wizard_data.date_to), format_data_left)
        worksheet.merge_range(row, col+9, row, col+10, 'Product', format_data_header)
        worksheet.merge_range(row, col + 11, row, col + 12, str(wizard_data.product_id.name or ''), format_data_left)

        row += 2

        worksheet.merge_range(row, col+4, row, col+7, 'IN', main_in_format)
        worksheet.merge_range(row, col+8, row, col+11, 'OUT', main_out_format)

        row += 1

        worksheet.write_string(row, col, 'Product', format_data_header)
        worksheet.write_string(row, col+1, 'Opening Quantity', format_data_header)
        worksheet.write_string(row, col+2, 'Reference Number', format_data_header)
        worksheet.write_string(row, col+3, 'Source Document', format_data_header)
        worksheet.write_string(row, col+4, 'Purchase', format_data_header)
        worksheet.write_string(row, col+5, 'Sale Return', format_data_header)
        worksheet.write_string(row, col+6, 'Issue Return', format_data_header)
        worksheet.write_string(row, col+7, 'Adjustment', format_data_header)
        worksheet.write_string(row, col+8, 'Purchase Return', format_data_header)
        worksheet.write_string(row, col+9, 'Sale', format_data_header)
        worksheet.write_string(row, col+10, 'Issue', format_data_header)
        worksheet.write_string(row, col+11, 'Adjustment', format_data_header)
        worksheet.write_string(row, col+12, 'Closing Quantity', format_data_header)

        row += 1

        for record in move_lines_record:
            opening = record.product_id.with_context({'to_date' : wizard_data.date_from}).qty_available
            closing = record.product_id.with_context(
                {'to_date': (wizard_data.date_to + timedelta(days=1))}).qty_available
            sale = 0.0
            purchase = 0.0
            issue = 0.0
            sale_ret = 0.0
            pur_ret = 0.0
            issue_ret = 0.0
            inventory_in = 0.0
            inventory_out = 0.0
            rec_check = 0
            if wizard_data.location_ids:
                if record.location_id.id in wizard_data.location_ids.ids or record.location_dest_id.id in wizard_data.location_ids.ids:
                    if record.location_id.usage == 'supplier' and record.location_dest_id.usage == 'internal':
                        rec_check += 1
                        purchase += record.qty_done
                    if record.location_id.usage == 'customer' and record.location_dest_id.usage == 'internal':
                        rec_check += 1
                        sale_ret += record.qty_done
                    if record.location_id.usage == 'production' and record.location_dest_id.usage == 'internal':
                        rec_check += 1
                        issue_ret += record.qty_done
                    if record.location_id.usage == 'inventory' and record.location_dest_id.usage == 'internal':
                        rec_check += 1
                        inventory_out += record.qty_done
                    if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'supplier':
                        rec_check += 1
                        pur_ret += record.qty_done
                    if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'customer':
                        rec_check += 1
                        sale += record.qty_done
                    if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'production':
                        rec_check += 1
                        issue += record.qty_done
                    if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'inventory':
                        rec_check += 1
                        inventory_in += record.qty_done
            else:
                if record.location_id.usage == 'supplier' and record.location_dest_id.usage == 'internal':
                    rec_check += 1
                    purchase += record.qty_done
                if record.location_id.usage == 'customer' and record.location_dest_id.usage == 'internal':
                    rec_check += 1
                    sale_ret += record.qty_done
                if record.location_id.usage == 'production' and record.location_dest_id.usage == 'internal':
                    rec_check += 1
                    issue_ret += record.qty_done
                if record.location_id.usage == 'inventory' and record.location_dest_id.usage == 'internal':
                    rec_check += 1
                    inventory_out += record.qty_done
                if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'supplier':
                    rec_check += 1
                    pur_ret += record.qty_done
                if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'customer':
                    rec_check += 1
                    sale += record.qty_done
                if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'production':
                    rec_check += 1
                    issue += record.qty_done
                if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'inventory':
                    rec_check += 1
                    inventory_in += record.qty_done
            if rec_check:
                worksheet.write_string(row, col, record.product_id.display_name or '', format_data_left)
                worksheet.write_number(row, col+1, opening, format_data_right)
                worksheet.write_string(row, col+2, record.reference or '', format_data_right)
                worksheet.write_string(row, col+3, record.origin or '', format_data_right)
                worksheet.write_number(row, col+4, purchase, format_data_right)
                worksheet.write_number(row, col+5, sale_ret, format_data_right)
                worksheet.write_number(row, col+6, issue_ret, format_data_right)
                worksheet.write_number(row, col+7, inventory_out, format_data_right)
                worksheet.write_number(row, col+8, pur_ret, format_data_right)
                worksheet.write_number(row, col+9, sale, format_data_right)
                worksheet.write_number(row, col+10, issue, format_data_right)
                worksheet.write_number(row, col+11, inventory_in, format_data_right)
                worksheet.write_number(row, col+12, closing, format_data_right)
                row += 1

        now = datetime.now()
        current_time = "{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        row += 1
        worksheet.write_string(row, col,  'Print Date', format_data_header)
        worksheet.write_string(row, col + 1, str(current_time), format_data_left)
