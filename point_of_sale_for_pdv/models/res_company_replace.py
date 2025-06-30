 # -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = 'res.company'
    
 
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='Departamento',
        required=False,  # Desactiva cualquier restricción
        store=False,     # Evita que se almacene en la base de datos
        compute=lambda self: None,  # Anula cualquier lógica
    )

    province_id = fields.Many2one(
        comodel_name='res.city',
        string='Provincia',
        required=False,
        store=False,
        compute=lambda self: None,
    )

    municipality_id = fields.Many2one(
        comodel_name='res.municipality',
        string='Municipio',
        required=False,
        store=False,
        compute=lambda self: None,
    )