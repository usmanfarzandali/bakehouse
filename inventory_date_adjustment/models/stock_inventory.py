# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    inventory_date = fields.Datetime(
        'Inventory Date', required=True,
        help="If the inventory adjustment is not validated, date at which the theoritical quantities have been checked.\n"
             "If the inventory adjustment is validated, date at which the inventory adjustment has been validated.")
    days_approval = fields.Integer("Inventory Days Approval")

    @api.model
    def create(self, vals):
        result = super(StockInventory, self).create(vals)
        days_approval = 0
        inv_date = datetime.datetime.strptime(vals['inventory_date'], '%Y-%m-%d %H:%M:%S')
        if self.env['ir.config_parameter'].sudo().get_param('inventory_date.days_approval'):
            days_approval = int(self.env['ir.config_parameter'].sudo().get_param('inventory_date.days_approval'))
        if days_approval:
            current_Date_days = (datetime.datetime.today()).day
            current_Date_month = (datetime.datetime.today()).month
            inv_Date_days = inv_date.day
            inv_Date_month = inv_date.month
            if inv_Date_month != current_Date_month:
                if inv_Date_month == current_Date_month - 1 and current_Date_days < days_approval:
                    pass
                elif inv_Date_month == current_Date_month - 1 and current_Date_days > days_approval:
                    raise UserError(_('Your Permission Days are Expired, Kindly Contact Your Admin For Permission'))
                else:
                    raise UserError(_('Your Permission Days are Expired, Kindly Contact Your Admin For Permission'))
        return result

    def _action_done(self):
        res = super(StockInventory, self)._action_done()
        self.write({'date': self.inventory_date})
        if self.move_ids:
            for record in self.move_ids:
                record.write({'date': self.inventory_date})
                for line in record.move_line_ids:
                    line.write({'date': self.inventory_date})
        return res


class InvDateSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    days_approval = fields.Integer("Inventory Days Approval")

    @api.model
    def get_values(self):
        res = super(InvDateSettings, self).get_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        days_approval = (config_parameter.get_param('inventory_date.days_approval'))
        res.update(days_approval=int(days_approval))
        return res

    def set_values(self):
        super(InvDateSettings, self).set_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        config_parameter.set_param("inventory_date.days_approval", self.days_approval)
