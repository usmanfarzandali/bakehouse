# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import timedelta, date, datetime
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class PosWReport(models.TransientModel):
    _name = 'w.report.wizard'
    _description = "POS W Report Wizard"

    pos_sessions_ids = fields.Many2one('pos.session', string="POS Session( IDs )",
                                       domain="[('state', 'in', ['closed'])]", required=True)
    reports_type = fields.Char('Report Type', readonly=True, default='PDF')
    company_ids = fields.Many2one('res.company', "Company")

    def generate_w_report(self):
        data = {'session_ids': self.pos_sessions_ids.ids, 'company': self.company_ids.id}
        return self.env.ref('pos_session_receipt.action_w_report_print').report_action([], data=data)


class ClosedSessionReceipt(models.AbstractModel):
    _name = 'report.pos_session_receipt.receipt_closed_session'
    _description = 'Closed Session Point of Sale Details'

    @api.model
    def get_sale_receipt_details(self, sessions=False, company=False):
        if sessions:
            orders = self.env['pos.order'].search([
                ('session_id.state', 'in', ['closed']),
                ('session_id', 'in', sessions.ids)])

        user_currency = self.env.user.company_id.currency_id

        total = 0.0
        products_sold = {}
        total_tax = 0.0
        taxes = {}
        mypro = {}
        products = []
        categories_data = {}
        total_discount = 0.0
        return_total = 0.0
        categories_tot = []
        return_orders = 0
        total_orders = 0

        for order in orders:
            # if user_currency != order.pricelist_id.currency_id:
            # 	total += order.pricelist_id.currency_id._convert(order.amount_total, user_currency, order.company_id, order.date_order or fields.Date.today())
            # else:
            if order.amount_total > 0:
                total += order.amount_total
                total_orders += 1
            currency = order.session_id.currency_id

            total_tax = total_tax + order.amount_tax
            # for line in order.payment_ids:
            # 	if line.name:
            # 		if 'return' in line.name:
            # 			return_total += abs(line.amount)
            # 			return_orders += 1
            if order.amount_total < 0:
                return_total += abs(order.amount_total)
                return_orders += 1

            for line in order.lines:
                total_discount += line.qty * line.price_unit - line.price_subtotal

                category = line.product_id.pos_categ_id.name
                if category in categories_data:
                    old_subtotal = categories_data[category]['total']
                    categories_data[category].update({'total': old_subtotal + line.price_subtotal_incl, })
                else:
                    categories_data.update({
                        category: {
                            'name': category,
                            'total': line.price_subtotal_incl,
                        }
                    })

            categories_tot = list(categories_data.values())

        st_line_ids = self.env["pos.payment"].search([('pos_order_id', 'in', orders.ids)]).ids
        if st_line_ids:
            self.env.cr.execute("""
                SELECT ppm.name, sum(amount) total, COUNT(amount) count
                FROM pos_payment AS pp,
                pos_payment_method AS ppm
                WHERE  pp.payment_method_id = ppm.id 
                AND pp.id IN %s 
                GROUP BY ppm.name
                """, (tuple(st_line_ids),))
            payments = self.env.cr.dictfetchall()
            # print(payments)
        else:
            payments = []

        total_cash_amt = 0
        total_card_amt = 0
        total_card_doc = 0
        total_cash_doc = 0
        for pay in payments:
            if 'card' in pay['name'].lower():
                total_card_doc += pay['count']
                total_card_amt += pay['total']
            # print(pay['total'])
            # print(pay['count'])
            if 'cash' in pay['name'].lower():
                total_cash_amt += pay['total']
                total_cash_doc += pay['count']

        # print(total_card_doc, total_card_amt, total_cash_amt, total_cash_doc)

        # cash_register_balance_end_real

        sessions_name = []
        session_end_user = []
        cash_register_balance_end_real = []
        cash_real_difference = []
        cash_real_transactions = []
        sessions_user_id = []
        sessions_config_id = []
        sessions_start_at = []
        sessions_stop_at = []
        opening_balance = 0.0
        closing_balance = 0.0
        control_diff = 0.0
        for i in sessions:
            if i.cash_register_balance_start:
                opening_balance += i.cash_register_balance_start
                closing_balance += i.cash_register_balance_end_real
                control_diff += i.cash_register_difference
            # print('====================================================', i)
            # print('====================================================', i.cash_register_balance_end_real)
            # print('====================================================', i.cash_real_transaction)
            # print('====================================================', i.cash_real_difference)
            # print('====================================================', i.name)
            # print('====================================================', i.user_id.name)
            # print('====================================================', i.config_id.name)
            # print('====================================================', i.move_id.name)
            # print('====================================================', (i.start_at + timedelta(hours=5)))
            # print('====================================================', (i.stop_at + timedelta(hours=5)))
            # print('====================================================', i.session_end_user.name)
            sessions_name.append(i.name)
            sessions_user_id.append(i.user_id.name)
            sessions_config_id.append(i.config_id.name)
            sessions_start_at.append((i.start_at + timedelta(hours=5)))
            sessions_stop_at.append((i.stop_at + timedelta(hours=5)))
            cash_register_balance_end_real.append(i.cash_register_balance_end_real)
            cash_real_difference.append(i.cash_real_difference)
            cash_real_transactions.append(i.cash_real_transaction)
            session_end_user.append(i.session_end_user.name)

        num_sessions = ', '.join(map(str, sessions_name))
        sessions_user = ', '.join(map(str, sessions_user_id))
        sessions_config = ', '.join(map(str, sessions_config_id))
        sessions_start = ', '.join(map(str, sessions_start_at))
        sessions_stop = ', '.join(map(str, sessions_stop_at))
        cash_register_balance = ', '.join(map(str, cash_register_balance_end_real))
        cash_real_transaction = ', '.join(map(str, cash_real_transactions))
        session_end_by = ', '.join(map(str, session_end_user))

        statement_id = self.env['account.bank.statement'].search([('name', '=', num_sessions)])
        # print(statement_id)
        # print(statement_id.cashbox_end_id)
        # print(statement_id.cashbox_end_id.id)
        cashbox_id = self.env['account.cashbox.line'].search([('cashbox_id', '=', statement_id.cashbox_end_id.id)])
        cashbox_id = sorted(cashbox_id)
        # print(cashbox_id)

        coin_values = []
        coin_numbers = []
        denomination = {
            5000: 0,
            1000: 0,
            500: 0,
            100: 0,
            75: 0,
            50: 0,
            20: 0,
            10: 0,
            5: 0,
            2: 0,
            1: 0,
        }
        total_denomination = 0.0
        for cash_line in cashbox_id:
            denomination[cash_line.coin_value] = cash_line.number
            coin_values.append(cash_line.coin_value)
            coin_numbers.append(cash_line.number)
            total_denomination += cash_line.coin_value * cash_line.number

        # print('coin_value :: ', cash_line.coin_value, 'number :: ', cash_line.number)

        # sorted_x = sorted(denomination.items(), key=lambda kv: kv[1])
        # print(denomination)

        cash_difference_short = 0
        cash_difference_excess = 0


        # Closing Cash Deposit > As Per Software ---------> excess
        # Closing Cash Deposit < As Per Software ---------> short

        if (float(total_denomination) - float(cash_real_transaction)) > 0:
            cash_difference_excess = (float(total_denomination) - float(cash_real_transaction))
        if (float(total_denomination) - float(cash_real_transaction)) < 0:
            cash_difference_short = (float(total_denomination) - float(cash_real_transaction))



        # if cash_real_difference[0] > 0:
        #     cash_difference_excess = ', '.join(map(str, cash_real_difference))
        #
        # if cash_real_difference[0] < 0:
        #     cash_difference_short = ', '.join(map(str, cash_real_difference))

        if session_end_by == 'False':
            session_end_by = False
            # session_end_by = 'Aun'

        return {
            'session_end_by': session_end_by,
            'total_card_amt': total_card_amt,
            'total_cash_amt': total_cash_amt,
            'total_card_doc': int(total_card_doc),
            'total_cash_doc': int(total_cash_doc),
            'denomination': denomination,
            'total_denomination': total_denomination,
            'coin_values': coin_values,
            'coin_numbers': coin_numbers,
            'cash_real_transaction': float(cash_real_transaction),
            'cash_register_balance': float(cash_register_balance),
            'cash_difference_excess': float(cash_difference_excess),
            'cash_difference_short': float(cash_difference_short),
            'return_orders': int(return_orders),
            'total_orders': total_orders,
            'sessions_user_id': sessions_user,
            'sessions_config_id': sessions_config,
            'sessions_start_at': sessions_start,
            'sessions_stop_at': sessions_stop,
            'currency_precision': 1,
            'total_paid': user_currency.round(total),
            'payments': payments,
            'company_name': self.env.user.company_id.name,
            'taxes': float(total_tax),
            'num_sessions': num_sessions,
            'categories_data': categories_tot,
            'total_discount': total_discount,
            'print_date': datetime.now(),
            'return_total': return_total,
            'opening_balance': opening_balance,
            'closing_balance': closing_balance,
            'control_diff': control_diff,
            'company': company,
        }

    def _get_report_values(self, docids, data=None):

        # context = self._context
        # current_uid = context.get('uid')
        # user = self.env['res.users'].browse(current_uid)
        # print('\n\n', user.name, '\n\n')

        data = dict(data or {})
        sessions = self.env['pos.session'].browse(data['session_ids'])
        company = self.env['res.company'].browse(data['company'])
        data.update(self.get_sale_receipt_details(sessions, company))

        return data


class AccountBankStmtCashWizard(models.Model):
    _inherit = 'account.bank.statement.cashbox'

    @api.model
    def default_get(self, fields):
        vals = super(AccountBankStmtCashWizard, self).default_get(fields)
        if 'cashbox_lines_ids' not in fields:
            return vals
        config_id = self.env.context.get('default_pos_id')
        if config_id:
            config = self.env['pos.config'].browse(config_id)
            if config.last_session_closing_cashbox.cashbox_lines_ids:
                lines = config.last_session_closing_cashbox.cashbox_lines_ids
            else:
                lines = config.default_cashbox_id.cashbox_lines_ids

            lin = []
            if self.env.context.get('balance', False) == 'start':
                vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': li, 'number': li, 'subtotal': li}] for li in lin]
                # vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': line.coin_value, 'number': line.number, 'subtotal': line.subtotal}] for line in lines]
            else:
                vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': li, 'number': li, 'subtotal': li}] for li in lin]
                # vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': line.coin_value, 'number': 0, 'subtotal': 0.0}] for line in lines]
        print('\n\n', vals, '\n\n')
        return vals

    def set_default_cashbox(self):
        self.ensure_one()
        current_session = self.env['pos.session'].browse(self.env.context['pos_session_id'])
        lines = current_session.config_id.default_cashbox_id.cashbox_lines_ids
        context = dict(self._context)
        self.cashbox_lines_ids.unlink()
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 1, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 2, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 5, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 10, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 20, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 50, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 75, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 100, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 500, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 1000, 'number': 0, 'subtotal': 0}]]
        self.cashbox_lines_ids = [[0, 0, {'coin_value': 5000, 'number': 0, 'subtotal': 0}]]

        # self.cashbox_lines_ids = [[0, 0, {'coin_value': line.coin_value, 'number': line.number, 'subtotal': line.subtotal}] for line in lines]

        return {
            'name': _('Cash Control'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.bank.statement.cashbox',
            'view_id': self.env.ref('point_of_sale.view_account_bnk_stmt_cashbox_footer').id,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
            'res_id': self.id,
        }


class PosSession(models.Model):
    _inherit = 'pos.session'

    session_end_user = fields.Many2one('res.users', 'Session End By')

    def action_pos_session_validate(self):
        self._check_pos_session_balance()
        context = self._context
        current_uid = context.get('uid')
        current_user = self.env['res.users'].browse(current_uid)
        session_end_user = current_user
        self.session_end_user = session_end_user
        # print('\n\n', session_end_user, '\n\n')
        return self.action_pos_session_close()
