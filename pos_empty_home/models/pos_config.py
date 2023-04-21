
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    iface_empty_home = fields.Boolean(
        string="Empty Home",
        help="Hide products if no category is selected.",
        default=True,
    )
