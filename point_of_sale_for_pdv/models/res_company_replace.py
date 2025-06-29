# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    state_id = fields.Many2one(
        string='Departamento',
    )

    province_id = fields.Many2one(
        string='Provincia',
    )

    municipality_id = fields.Many2one(
        string='Municipio',
    )
