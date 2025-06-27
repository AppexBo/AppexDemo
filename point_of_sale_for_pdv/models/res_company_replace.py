# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = 'res.company'

    state_id = fields.Many2one(
        string='Departamento',
        comodel_name='res.country.state',

    )

    province_id = fields.Many2one(
        string='Provincia',
        comodel_name='res.city',
        copy=False,

    )
    
    municipality_id = fields.Many2one(
        string='Municipio',
        comodel_name='res.municipality',
        copy=False,

    )   