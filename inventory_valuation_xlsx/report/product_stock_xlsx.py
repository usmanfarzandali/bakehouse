from datetime import timedelta
from odoo import models
from datetime import datetime, time


class ProductRecord(models.AbstractModel):
    _name = 'report.inventory_valuation_xlsx.product_stock_template'
    _description = "Product Stock Report"
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

        worksheet = workbook.add_worksheet('Products Stock Report')

        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:C', 15)

        worksheet.merge_range('A2:C3', 'Products Stock Report', main_merge_format)

        row = 5
        col = 0

        domain = [('state', '=', 'done'), ('product_id.type', '=', 'product')]
        if wizard_data.companies:
            domain += [('company_id', 'in', wizard_data.companies.ids)]

        product_records = self.env['product.product'].search([])

        worksheet.write_string(row, col,  'Company', format_data_header)
        worksheet.merge_range(row, col + 1, row, col + 2, str(wizard_data.companies.mapped('name') or ''),
                              format_data_left)
        row += 1
        worksheet.write_string(row, col, 'User', format_data_header)
        current_user = self.env.user.name
        worksheet.write_string(row, col + 1, str(current_user), format_data_left)
        row += 1
        worksheet.write_string(row, col, 'Date From', format_data_header)
        worksheet.write_string(row, col+1, str(wizard_data.date_from), format_data_left)
        row += 1
        worksheet.write_string(row, col, 'Date To', format_data_header)
        worksheet.write_string(row, col+1, str(wizard_data.date_to), format_data_left)


        row += 2

        worksheet.write_string(row, col, 'Product', format_data_header)
        worksheet.write_string(row, col+1, 'Opening', format_data_header)
        worksheet.write_string(row, col+2, 'Closing', format_data_header)

        row += 1

        for product in product_records:
            opening = 0.0
            closing = 0.0
            prod_opening_balance = self.env['stock.valuation.layer'].search([('product_id', '=', product.id),
                                                                             ('create_date', '<=',
                                                                              wizard_data.date_from)])
            prod_closing_balance = self.env['stock.valuation.layer'].search([('product_id', '=', product.id),
                                                                             (
                                                                             'create_date', '<=', wizard_data.date_to)])
            for stock in prod_opening_balance:
                opening += stock.quantity
            for stock in prod_closing_balance:
                closing += stock.quantity
            if closing != 0.0:
                worksheet.write_string(row, col, product.display_name or '', format_data_left)
                worksheet.write_number(row, col+1, opening, format_data_right)
                worksheet.write_number(row, col+2, closing, format_data_right)
                row += 1

        now = datetime.now()
        current_time = "{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        row += 1
        worksheet.write_string(row, col, 'Print Date', format_data_header)
        worksheet.write_string(row, col + 1, str(current_time), format_data_left)





        ##########################################33
class Product_Stock_Pdf(models.AbstractModel):
    _name = 'report.inventory_valuation_xlsx.product_stock_pdf'

    def _get_report_values(self, docids, data=None):


        data = self.env['inventory.valuation.wizard'].browse(self.env.context.get('active_ids'))

        wizard_data = self.env['inventory.valuation.wizard'].browse(self.env.context.get('active_ids'))

        domain = [('state', '=', 'done'), ('product_id.type', '=', 'product')]
        if wizard_data.companies:
            domain += [('company_id', 'in', wizard_data.companies.ids)]

        product_records = self.env['product.product'].search([])
        data_list = []
        for product in product_records:
            opening = 0.0
            closing = 0.0
            prod_opening_balance = self.env['stock.valuation.layer'].search([('product_id', '=', product.id),
                                                                             ('create_date', '<=',
                                                                              wizard_data.date_from)])
            prod_closing_balance = self.env['stock.valuation.layer'].search([('product_id', '=', product.id),
                                                                             (
                                                                                 'create_date', '<=',
                                                                                 wizard_data.date_to)])

            for stock in prod_opening_balance:
                opening += stock.quantity
            for stock in prod_closing_balance:
                closing += stock.quantity
            if closing != 0.0:

                data_list.append({
                    'product': product.display_name or '',
                    'opening': opening or '',
                    'closing': closing or '',

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
