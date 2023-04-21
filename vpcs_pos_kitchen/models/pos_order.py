# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class PosOrder(models.Model):
    _inherit = 'pos.order'


    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res.update({'priority': ui_order.get('priority'), 'old_priority': ui_order.get('old_priority')})
        return res

    def _get_fields_for_draft_order(self):
        res = super(PosOrder, self)._get_fields_for_draft_order()
        res.append('priority')
        res.append('old_priority')
        return res

    def _get_fields_for_order_line(self):
        res = super(PosOrder, self)._get_fields_for_order_line()
        res.append('state')
        res.append('has_qty_change')
        res.append('cid')
        return res


    priority = fields.Selection(
            [('low', 'Low'), ('normal', 'Normal'), ('high', 'High')],
            string="Priority", default="normal")
    old_priority = fields.Selection(
            [('low', 'Low'), ('normal', 'Normal'), ('high', 'High')],
            string="Old Priority")


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    state = fields.Selection(
        [('new', 'New'), ('Cooking', 'Cooking'), ('ready to serve', 'Ready To Serve'),
        ('done', 'Done')], string="States")
    has_qty_change = fields.Boolean(string="Qty Change Flag")
    cid = fields.Char(string="cid")