# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """This function is inherit for effective date change"""
        transfer_date = self.date_done
        res = super(StockPicking, self).button_validate()
        self.date_done = transfer_date
        if self.move_lines:
            self.move_lines.update({'date': self.date_done})
            if self.move_lines.account_move_ids:
                for record in self.move_lines.account_move_ids:
                    pick_date = (self.date_done).date()
                    record.button_draft()
                    record.name = False
                    record.update({'date': pick_date})
                    record.action_post()
            if self.move_line_ids:
                for line in self.move_line_ids:
                    line.date = self.date_done
        return res
