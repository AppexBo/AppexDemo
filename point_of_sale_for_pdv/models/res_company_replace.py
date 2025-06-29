# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    state_id = fields.char(
        string='Departamento',
    )

    province_id = fields.char(
        string='Provincia',
    )

    municipality_id = fields.char(
        string='Municipio',
    )
