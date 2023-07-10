from odoo import models, api, fields, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('purchase_manager', 'Purchase Manager'),
                                            ('admin', 'Administrator'),
                                            ('purchase', 'Purchase Order')])


    def button_confirm(self):
        if self.user_id.has_group('aps_purchase_approval.group_purchase_user') \
                and not self.user_id.has_group('aps_purchase_approval.group_purchase_manager') \
                and not self.user_id.has_group('aps_purchase_approval.group_purchase_administrator'):
            if self.user_id.partner_id.pur_approval_amount < self.amount_total:
                self.state = 'purchase_manager'
            else:
                return super(PurchaseOrder, self).button_confirm()
        elif self.user_id.has_group('aps_purchase_approval.group_purchase_manager') \
                and not self.user_id.has_group('aps_purchase_approval.group_purchase_administrator'):
            if self.user_id.partner_id.pur_approval_amount < self.amount_total:
                self.state = 'admin'
            else:
                return super(PurchaseOrder, self).button_confirm()
        elif self.user_id.has_group('aps_purchase_approval.group_purchase_administrator'):
            return super(PurchaseOrder, self).button_confirm()
        else:
            raise UserError(_("You Don't Have Access To Confirm Purchase Order"))

    def action_confirm_manager(self):
        if self.user_id.partner_id.pur_approval_amount < self.amount_total:
            self.state = 'admin'
        else:
            self.state = 'draft'
            return super(PurchaseOrder, self).button_confirm()

    def action_confirm_admin(self):
        self.state = 'draft'
        return super(PurchaseOrder, self).button_confirm()
