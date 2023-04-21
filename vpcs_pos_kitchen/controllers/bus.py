# -*- coding: utf-8 -*

from odoo.addons.bus.controllers.main import BusController
from odoo.http import request


class PosSessionBusController(BusController):
    # --------------------------
    # Extends BUS Controller Poll
    # --------------------------
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, 'pos.order.synch'))
        return super(PosSessionBusController, self)._poll(dbname, channels, last, options)
