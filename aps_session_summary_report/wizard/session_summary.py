# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from datetime import timedelta, date, datetime


class SessionSummary(models.TransientModel):
    _name = "session.summary.wizard"
    _description = "session summary Wizard"

    date_from = fields.Datetime("Date From", required=True)
    date_to = fields.Datetime("Date To", required=True)

    def generate_partner_ledger_pdf(self):
        # print("tet.......", self.read()[0]),
        # all_sessions = self.env['pos.session'].search_read([])
        # print('\n\n All Sessions ', all_sessions, '\n\n')
        # payments = self.env['pos.payment'].search_read([])
        # print('\n\npayments', payments, '\n\n')

        # date_from = str(self.date_from) + ' 00:00:00'
        # date_to = str(self.date_to) + ' 23:59:59'
        date_from = str(self.date_from)
        date_to = str(self.date_to)
        # print('\n\nWizard Date From', date_from, '\n\n')
        # print('\n\nWizard Date To', date_to, '\n\n')

        sessions = self.env['pos.session'].search([
            ('stop_at', '>=', date_from),
            ('stop_at', '<=', date_to),
            ('state',   '=',  'closed')
        ])
        # print('\n\nsessions', sessions, '\n\n')

        all_sessions_data = []
        for session in sessions:
            config_id = session.config_id.name
            session_name = session.name
            opened_by = session.user_id.name
            closed_by = session.session_end_user.name
            cash_deposited = session.cash_register_balance_end_real

            session_sale_payments = {}
            # sale_cash_payment = 0.0
            sale_card_payment = 0.0
            sale_payment_method = session.payment_method_ids
            for payment_method in sale_payment_method:
                result = self.env['pos.payment'].read_group(
                    [
                        ('session_id', '=', session.id),
                        ('payment_method_id', '=', payment_method.id)
                    ],
                    ['amount'],
                    ['session_id']
                )
                if result:
                    if 'card' in payment_method.name.lower():
                        sale_card_payment = result[0]['amount']
                        session_sale_payments['card'] = sale_card_payment
                    # elif 'cash' in payment_method.name.lower():
                    #     sale_cash_payment = result[0]['amount']
                    #     session_sale_payments['cash'] = sale_cash_payment

            sales_order_count = 0
            sales_payments = 0.0
            sales_return_count = 0
            sales_return_payments = 0.0
            orders = self.env['pos.order'].search([
                ('session_id.state', 'in', ['closed']),
                ('session_id', 'in', session.ids)
            ])
            for order in orders:
                if order.amount_total >= 0:
                    sales_payments += abs(order.amount_total)
                    sales_order_count += 1
                if order.amount_total < 0:
                    sales_return_payments += abs(order.amount_total)
                    sales_return_count += 1

            sales_order_payments = sales_payments - sale_card_payment
            net_sale_count = (sales_order_count + sales_return_count)
            net_cash_sales = (sales_order_payments - sales_return_payments)
            net_sale_payments = (net_cash_sales + sale_card_payment)

            short_excess = 0.0
            if cash_deposited:
                cash_subtract = (cash_deposited - net_cash_sales)
                if cash_subtract > 0:
                    short_excess = cash_subtract
                elif cash_subtract < 0:
                    short_excess = cash_subtract
                elif cash_subtract == 0:
                    short_excess = cash_subtract

            # print('\n\nPOS.Session(id) =\t',    session)
            # print('Session Closing =\t',        (session.stop_at + timedelta(hours=5)))
            # print('POS Session Name =\t',       config_id)
            # print('POS Session ID =\t',         session_name)
            # print('Session Opened By =\t',      opened_by)
            # print('Session Closed By =\t',      closed_by)
            # print('Sale Order Count =\t',       sales_order_count)
            # print('Sale Order Payment =\t',     sales_order_payments)
            # print('Card Order Payment =\t',     sale_card_payment)
            # print('Sale Return Count =\t',      sales_return_count)
            # print('Sale Return Payment =\t',    sales_return_payments)
            # print('Net Sales Count =\t',         net_sale_count)
            # print('Net Sales Cash =\t',          net_cash_sales)
            # print('Net Sales Credit =\t',        sale_card_payment)
            # print('Net Sales Total =\t',         net_sale_payments)
            # print('Cash Deposited =\t',         cash_deposited)
            # print('(Short)/Excess =\t',         short_excess)
            # print('Session Orders =\t',       orders)

            all_sessions_data.append(
                {
                    'config_id':                config_id,
                    'session_name':             session_name,
                    'opened_by':                opened_by,
                    'closed_by':                closed_by,
                    'sales_order_count':        sales_order_count,
                    'sale_cash_payment':        sales_order_payments,
                    'sale_card_payment':        sale_card_payment,
                    'session_sale_payments':    session_sale_payments,
                    'sales_return_count':       sales_return_count,
                    'sales_return_payments':    sales_return_payments,
                    'net_sale_count':           net_sale_count,
                    'net_cash_sales':           net_cash_sales,
                    'net_sale_payments':        net_sale_payments,
                    'cash_deposited':           cash_deposited,
                    'short_excess':             short_excess,
                }
            )

        # for sessions in all_sessions_data:
        #     print('\n==========================================================')
        #     print('Session(', sessions['session_name'], ')  = ', sessions)
        #     print('==========================================================')

        data = {
            'date_from': (self.date_from + timedelta(hours=5)),
            'date_to': (self.date_to + timedelta(hours=5)),
            'sessions': all_sessions_data,
        }
        return self.env.ref('aps_session_summary_report.session_summary_report_pdf')\
            .with_context(landscape=True).report_action(self, data=data)
