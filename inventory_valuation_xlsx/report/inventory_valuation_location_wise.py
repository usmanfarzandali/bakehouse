from datetime import timedelta
from odoo import models
from datetime import datetime, time


class InventoryLocationWise(models.AbstractModel):
    _name = 'report.inventory_valuation_xlsx.inventory_location_template'
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
        worksheet.set_column('B:H', 13)

        worksheet.merge_range('A2:H3', 'Inventory OPSI Report', main_merge_format)

        row = 5
        col = 0

        domain = [('state', '=', 'done'),('product_id.type', '=', 'product')]
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
        worksheet.write_string(row, col + 6, 'Company', format_data_header)
        worksheet.write_string(row, col + 7, str(wizard_data.companies.mapped('name') or ''), format_data_left)
        row += 1
        worksheet.write_string(row, col, 'Date To', format_data_header)
        worksheet.write_string(row, col+1, str(wizard_data.date_to), format_data_left)
        worksheet.write_string(row, col+6, 'Product', format_data_header)
        worksheet.write_string(row, col + 7, str(wizard_data.product_id.name or ''), format_data_left)

        row += 2

        worksheet.write_string(row, col, 'Product', format_data_header)
        worksheet.write_string(row, col+1, 'Opening Quantity', format_data_header)
        worksheet.write_string(row, col+2, 'Reference Number', format_data_header)
        worksheet.write_string(row, col+3, 'Source Document', format_data_header)
        worksheet.write_string(row, col+4, 'From', format_data_header)
        worksheet.write_string(row, col+5, 'To', format_data_header)
        worksheet.write_string(row, col+6, 'Quantity Done', format_data_header)
        worksheet.write_string(row, col+7, 'Closing Quantity', format_data_header)

        row += 1

        loc_filt_record = []
        for record in move_lines_record:
            if record.location_id.id in wizard_data.location_ids.ids or record.location_dest_id.id in wizard_data.location_ids.ids:
                loc_filt_record.append(record)
        for record in loc_filt_record:
            opening = record.product_id.with_context({'to_date' : wizard_data.date_from}).qty_available
            closing = record.product_id.with_context(
                {'to_date': (wizard_data.date_to + timedelta(days=1))}).qty_available
            worksheet.write_string(row, col, record.product_id.display_name or '', format_data_left)
            worksheet.write_number(row, col+1, opening, format_data_right)
            worksheet.write_string(row, col+2, record.reference or '', format_data_right)
            worksheet.write_string(row, col+3, record.origin or '', format_data_right)
            worksheet.write_string(row, col + 4, str(record.location_id.name), format_data_right)
            worksheet.write_string(row, col + 5, str(record.location_dest_id.name), format_data_right)
            worksheet.write_number(row, col+6, record.qty_done, format_data_right)
            worksheet.write_number(row, col+7, closing, format_data_right)
            row += 1

        now = datetime.now()
        current_time = "{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        row += 1
        worksheet.write_string(row, col,  'Print Date', format_data_header)
        worksheet.write_string(row, col + 1, str(current_time), format_data_left)








######################################

class InvSummaryPdf(models.AbstractModel):
    _name = 'report.inventory_valuation_xlsx.inv_value_location_pdf'

    def _get_report_values(self, docids, data=None):

        data = self.env['inventory.valuation.wizard'].browse(self.env.context.get('active_ids'))

        wizard_data = self.env['inventory.valuation.wizard'].browse(self.env.context.get('active_ids'))
        domain = [('state', '=', 'done'), ('product_id.type', '=', 'product')]
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


        data_list = []
        loc_filt_record = []
        for record in move_lines_record:
            if record.location_id.id in wizard_data.location_ids.ids or record.location_dest_id.id in wizard_data.location_ids.ids:
                loc_filt_record.append(record)
        for record in loc_filt_record:
            opening = record.product_id.with_context({'to_date': wizard_data.date_from}).qty_available
            closing = record.product_id.with_context(
                {'to_date': (wizard_data.date_to + timedelta(days=1))}).qty_available

            data_list.append({
                'prod_name':record.product_id.display_name or '',
                'opening': opening,
                'opening_bal': record.reference or '',
                'purchase':record.origin or '',
                'purchase_bal':  str(record.location_id.name),
                'sale_ret':  str(record.location_dest_id.name),
                'sale_ret_bal': record.qty_done,
                'issue_ret': closing,


            })

        docs = self.env['inventory.valuation.wizard'].browse(docids)

        invoice_records_multi = self.env['stock.move.line'].search([])
        invoice_records = invoice_records_multi[0]

        now = datetime.now()
        current_time = "{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        Uuser = self.env.user.name
        # for com in wizard_data.companies:
        #     comp = com[0]

        return {
            'doc_ids': docids,
            'doc_model': 'inventory.valuation.wizard',
            'data': data_list,
            'wizard_data': wizard_data,
            'DDate': current_time,
            'Uuser': Uuser,
            # 'comp': comp,
        }
