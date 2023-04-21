from odoo import models, api, fields, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('sale_manager', 'Sale Manager'),
                                            ('admin', 'Administrator'),
                                            ('sale', 'Sale Order')])

    def action_confirm(self):
        if self.user_id.has_group('aps_sale_approval.group_sale_user') \
                and not self.user_id.has_group('aps_sale_approval.group_sale_manager') \
                and not self.user_id.has_group('aps_sale_approval.group_sale_administrator'):
            if self.user_id.partner_id.approval_amount < self.amount_total:
                self.state = 'sale_manager'
            else:
                return super(SaleOrder, self).action_confirm()
        elif self.user_id.has_group('aps_sale_approval.group_sale_manager') \
                and not self.user_id.has_group('aps_sale_approval.group_sale_administrator'):
            if self.user_id.partner_id.approval_amount < self.amount_total:
                self.state = 'admin'
            else:
                return super(SaleOrder, self).action_confirm()
        elif self.user_id.has_group('aps_sale_approval.group_sale_administrator'):
            return super(SaleOrder, self).action_confirm()
        else:
            raise UserError(_("You Don't Have Access To Confirm Sale Order"))

    def action_confirm_manager(self):
        if self.user_id.partner_id.approval_amount < self.amount_total:
            self.state = 'admin'
        else:
            return super(SaleOrder, self).action_confirm()

    def action_confirm_admin(self):
        return super(SaleOrder, self).action_confirm()