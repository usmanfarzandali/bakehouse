
from datetime import timedelta
from odoo import api, fields, models, tools, _
from datetime import datetime, time


class SessionSummary(models.AbstractModel):
    _name = 'report.aps_session_summary_report.report_session_summary'

    def _get_report_values(self, docids, data=None):
        # global DDate
        docs = self.env['pos.session'].browse(docids)

        # Getting current company
        company = self.env.company

        now = datetime.now()
        current_time ="{:%Y-%m-%d %H_%M_%S}".format(now + timedelta(hours=5))
        Uuser = self.env.user.name
        # comp = wizard_data.companies.name

        return {
            'doc_ids': docids,
            'doc_model': 'pos.session',
            # 'wizard_data': wizard_data,
            'DDate': current_time,
            'Uuser': Uuser,
            'docs': docs,
            # 'session': session,

        }
