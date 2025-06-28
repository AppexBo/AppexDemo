# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime
import logging
from pytz import timezone
import pytz
_logger = logging.getLogger(__name__)


class L10nBoPos(models.Model):
    _inherit = "l10n.bo.pos"
    _description = "Nuevos campos en el punto de venta"

    company_id = fields.Many2one(
        string='Compañia',
        comodel_name='res.company',
        required=True,
        default=lambda self: self.env.company,
        readonly=True

    )
    state_id = fields.Many2one(
        string='Departamento',
        comodel_name='res.country.state',
        domain=lambda self: [
            ('country_id', '=', self.env.company.country_id.id)]
    )

    @api.onchange('state_id')
    def set_company_state(self):
        company = self.env.company
        state = self.env['res.country.state'].search(
            [('name', '=', self.state_id.name)], limit=1)
        if not state:
            raise UserError("No se encontró el departamento Santa Cruz")
        company.state_id = state.id
    province_id = fields.Many2one(
        string='Provincia',
        comodel_name='res.city',
        copy=False
    )

    municipality_id = fields.Many2one(
        string='Municipio',
        comodel_name='res.municipality',
        copy=False,
    )

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self._origin and self.state_id and self.state_id != self._origin.state_id:
            self.province_id = False
            self.municipality_id = False

    def getMunicipalityName(self):
        if self.municipality_id:
            return self.municipality_id.name
        raise UserError(
            'El punto de venta seleccionado no tiene municipio asignado.')
