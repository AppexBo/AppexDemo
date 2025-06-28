from odoo import api, models, fields
from odoo.exceptions import UserError
import pytz


class AccountMoveParams(models.Model):
    _inherit = 'account.move'

    def getMunicipality(self):
        return self.pos_id.getMunicipalityName()