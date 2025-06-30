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
    state_id_nuevo = fields.Many2one(
        string='Departamento',
        comodel_name='res.country.state',
        domain=lambda self: [
            ('country_id', '=', self.env.company.country_id.id)]
    )

    province_id_nuevo = fields.Many2one(
        string='Provincia',
        comodel_name='res.city',
        copy=False
    )

    municipality_id_nuevo = fields.Many2one(
        string='Municipio',
        comodel_name='res.municipality',
        copy=False,
    )

    @api.onchange('state_id_nuevo')
    def _onchange_state_id(self):
        if self._origin and self.state_id_nuevo and self.state_id_nuevo != self._origin.state_id_nuevo:
            self.province_id_nuevo = False
            self.municipality_id_nuevo = False

    def getMunicipalityName(self):
        if self.municipality_id_nuevo:
            return self.municipality_id_nuevo.name
        raise UserError(
            'El punto de venta seleccionado no tiene municipio asignado.')
