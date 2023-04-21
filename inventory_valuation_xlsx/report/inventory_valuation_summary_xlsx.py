from datetime import timedelta
from odoo import models
from datetime import datetime, time

class CODPaymentXlsx(models.AbstractModel):
    _name = 'report.inventory_valuation_xlsx.inv_valuation_summary_template'
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

        worksheet = workbook.add_worksheet('Product Summary  Report')

        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:K', 12)

        worksheet.merge_range('A2:K3', 'Product Summary  Report', main_merge_format)

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

        worksheet.write_string(row, col, 'User', format_data_header)
        current_user = self.env.user.name
        worksheet.write_string(row, col + 1, str(current_user), format_data_left)
        row += 1
        worksheet.write_string(row, col, 'Date From', format_data_header)
        worksheet.write_string(row, col+1, str(wizard_data.date_from), format_data_left)
        worksheet.merge_range(row, col + 7, row, col + 8, 'Company', format_data_header)
        worksheet.merge_range(row, col + 9, row, col + 10, str(wizard_data.companies.mapped('name') or ''), format_data_left)
        row += 1
        worksheet.write_string(row, col, 'Date To', format_data_header)
        worksheet.write_string(row, col+1, str(wizard_data.date_to), format_data_left)
        worksheet.merge_range(row, col+7, row, col+8, 'Product', format_data_header)
        worksheet.merge_range(row, col + 9, row, col + 10, str(wizard_data.product_id.name or ''), format_data_left)

        row += 2

        worksheet.merge_range(row, col+2, row, col+5, 'IN', main_in_format)
        worksheet.merge_range(row, col+6, row, col+9, 'OUT', main_out_format)

        row += 1

        worksheet.write_string(row, col, 'Product', format_data_header)
        worksheet.write_string(row, col+1, 'Opening Quantity', format_data_header)
        worksheet.write_string(row, col+2, 'Purchase', format_data_header)
        worksheet.write_string(row, col+3, 'Sale Return', format_data_header)
        worksheet.write_string(row, col+4, 'Issue Return', format_data_header)
        worksheet.write_string(row, col+5, 'Adjustment', format_data_header)
        worksheet.write_string(row, col+6, 'Purchase Return', format_data_header)
        worksheet.write_string(row, col+7, 'Sale', format_data_header)
        worksheet.write_string(row, col+8, 'Issue', format_data_header)
        worksheet.write_string(row, col+9, 'Adjustment', format_data_header)
        worksheet.write_string(row, col+10, 'Closing Quantity', format_data_header)

        row += 1

        prod_list = []
        loc_filt_record = []
        prod_sum_list = []
        for product in move_lines_records:
            prod_sub_lis = []
            if product.product_id.id not in prod_list:
                prod_list.append(product.product_id.id)
                prod_data = move_lines_records.search([('product_id', '=', product.product_id.id),
                                                       ('date', '>=', wizard_data.date_from),
                                                       ('date', '<=', wizard_data.date_to)])
                for record in prod_data:
                    if record.location_id.name == 'Stock' or record.location_dest_id.name == 'Stock':
                        loc_filt_record.append(record)
                prod_name = ''
                opening = 0.0
                closing = 0.0
                sale = 0.0
                purchase = 0.0
                issue = 0.0
                sale_ret = 0.0
                pur_ret = 0.0
                issue_ret = 0.0
                inventory_in = 0.0
                inventory_out = 0.0
                for record in loc_filt_record:
                    prod_name = record.product_id.display_name
                    opening = record.product_id.with_context({'to_date' : wizard_data.date_from}).qty_available
                    closing = record.product_id.with_context({'to_date' : (wizard_data.date_to + timedelta(days=1))}).qty_available
                    rec_name = record.reference
                    sub_str = rec_name.split("/")
                    inv_sub_str = rec_name.split(":")
                    if len(sub_str) > 2:
                        if sub_str[1] == 'INT':
                            if record.location_id.name == 'Stock':
                                pur_ret += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                purchase += record.qty_done
                        if sub_str[1] == 'OUT':
                            if record.location_id.name == 'Stock':
                                sale += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                sale_ret += record.qty_done
                        if sub_str[1] == 'IN':
                            if record.location_dest_id.name == 'Stock':
                                sale_ret += record.qty_done
                        if sub_str[1] == 'DCC':
                            if record.location_id.name == 'Stock':
                                issue += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                issue_ret += record.qty_done
                        if sub_str[1] == 'SSC':
                            if record.location_id.name == 'Stock':
                                issue += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                issue_ret += record.qty_done
                        if sub_str[1] == 'PMC':
                            if record.location_id.name == 'Stock':
                                issue += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                issue_ret += record.qty_done
                    else:
                        if inv_sub_str[0] == 'INV' or rec_name == 'Product Quantity Updated':
                            if record.location_id.name == 'Stock':
                                inventory_in += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                inventory_out += record.qty_done
                prod_sub_lis = [prod_name, opening, purchase, sale_ret, issue_ret, inventory_out, pur_ret, sale, issue, inventory_in, closing]
                prod_sum_list.append(prod_sub_lis)

        for lis_rec in prod_sum_list:
            worksheet.write_string(row, col, lis_rec[0] or '', format_data_left)
            worksheet.write_number(row, col+1, lis_rec[1], format_data_right)
            worksheet.write_number(row, col+2, lis_rec[2], format_data_right)
            worksheet.write_number(row, col+3, lis_rec[3], format_data_right)
            worksheet.write_number(row, col+4, lis_rec[4], format_data_right)
            worksheet.write_number(row, col+5, lis_rec[5], format_data_right)
            worksheet.write_number(row, col+6, lis_rec[6], format_data_right)
            worksheet.write_number(row, col+7, lis_rec[7], format_data_right)
            worksheet.write_number(row, col+8, lis_rec[8], format_data_right)
            worksheet.write_number(row, col+9, lis_rec[9], format_data_right)
            worksheet.write_number(row, col+10, lis_rec[10], format_data_right)
            row += 1

        now = datetime.now()
        current_time = "{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        row += 1
        worksheet.write_string(row, col, 'Print Date', format_data_header)
        worksheet.write_string(row, col + 1, str(current_time), format_data_left)










        #######################################
class inventory_valuation_pdf(models.AbstractModel):
    _name = 'report.inventory_valuation_xlsx.report_supplier_id_card'

    def _get_report_values(self, docids, data=None):
        data = self.env['inventory.valuation.wizard'].browse(self.env.context.get('active_ids'))
        wizard_data = self.env['inventory.valuation.wizard'].browse(self.env.context.get('active_ids'))

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



        prod_list = []
        loc_filt_record = []
        prod_sum_list = []
        data_list = []
        for product in move_lines_records:
            prod_sub_lis = []
            if product.product_id.id not in prod_list:
                prod_list.append(product.product_id.id)
                prod_data = move_lines_records.search([('product_id', '=', product.product_id.id),
                                                       ('date', '>=', wizard_data.date_from),
                                                       ('date', '<=', wizard_data.date_to)])
                for record in prod_data:
                    if record.location_id.name == 'Stock' or record.location_dest_id.name == 'Stock':
                        loc_filt_record.append(record)
                prod_name = ''
                opening = 0.0
                closing = 0.0
                sale = 0.0
                purchase = 0.0
                issue = 0.0
                sale_ret = 0.0
                pur_ret = 0.0
                issue_ret = 0.0
                inventory_in = 0.0
                inventory_out = 0.0
                for record in loc_filt_record:
                    prod_name = record.product_id.display_name
                    opening = record.product_id.with_context({'to_date': wizard_data.date_from}).qty_available
                    closing = record.product_id.with_context(
                        {'to_date': (wizard_data.date_to + timedelta(days=1))}).qty_available
                    rec_name = record.reference
                    sub_str = rec_name.split("/")
                    inv_sub_str = rec_name.split(":")
                    if len(sub_str) > 2:
                        if sub_str[1] == 'INT':
                            if record.location_id.name == 'Stock':
                                pur_ret += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                purchase += record.qty_done
                        if sub_str[1] == 'OUT':
                            if record.location_id.name == 'Stock':
                                sale += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                sale_ret += record.qty_done
                        if sub_str[1] == 'IN':
                            if record.location_dest_id.name == 'Stock':
                                sale_ret += record.qty_done
                        if sub_str[1] == 'DCC':
                            if record.location_id.name == 'Stock':
                                issue += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                issue_ret += record.qty_done
                        if sub_str[1] == 'SSC':
                            if record.location_id.name == 'Stock':
                                issue += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                issue_ret += record.qty_done
                        if sub_str[1] == 'PMC':
                            if record.location_id.name == 'Stock':
                                issue += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                issue_ret += record.qty_done
                    else:
                        if inv_sub_str[0] == 'INV' or rec_name == 'Product Quantity Updated':
                            if record.location_id.name == 'Stock':
                                inventory_in += record.qty_done
                            if record.location_dest_id.name == 'Stock':
                                inventory_out += record.qty_done
                prod_sub_lis = [prod_name, opening, purchase, sale_ret, issue_ret, inventory_out, pur_ret, sale, issue,
                                inventory_in, closing]
                prod_sum_list.append(prod_sub_lis)

        for lis_rec in prod_sum_list:
            data_list.append({
                'prod_name': lis_rec[0] or '',
                'opening': lis_rec[1],
                'purchase': lis_rec[2],
                'sale_ret': lis_rec[3],
                'issue_ret': lis_rec[4],
                'inventory_out': lis_rec[5],
                'pur_ret': lis_rec[6],
                'sale': lis_rec[7],
                'issue': lis_rec[8],
                'inventory_in': lis_rec[9],
                'closing': lis_rec[10],
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