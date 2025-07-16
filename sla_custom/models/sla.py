from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sla_paused = fields.Boolean(string="SLA Pausado", default=True)
    sla_pause_start = fields.Datetime(string="Inicio de Pausa del SLA")
    sla_total_paused_time = fields.Float(
        string="Tiempo Total Pausado (Horas)", default=0.0)

    @api.model
    def create(self, vals):
        # Iniciar el ticket con el SLA pausado hasta que el cliente responda
        ticket = super(HelpdeskTicket, self).create(vals)
        ticket.sla_paused = True
        ticket.sla_pause_start = fields.Datetime.now()
        return ticket

    def write(self, vals):
        # Detectar cambios en el ticket y actualizar el estado del SLA
        res = super(HelpdeskTicket, self).write(vals)
        for ticket in self:
            if 'sla_paused' in vals or 'sla_pause_start' in vals:
                ticket.sla_status_ids._compute_sla_deadline()
        return res


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        # Crear el mensaje
        message = super(MailMessage, self).create(vals)

        # Verificar si el mensaje pertenece a un ticket
        if message.model == 'helpdesk.ticket' and message.res_id:
            ticket = self.env['helpdesk.ticket'].browse(message.res_id)
            is_employee = message.author_id.employee_ids

            if ticket:
                # Si el mensaje es del cliente (no empleado), reanudar el SLA
                if not is_employee:
                    if ticket.sla_paused:
                        # Calcular el tiempo pausado y actualizar
                        pause_start = ticket.sla_pause_start
                        if pause_start:
                            pause_duration = (fields.Datetime.now(
                            ) - pause_start).total_seconds() / 3600.0
                            ticket.sla_total_paused_time += pause_duration
                        ticket.sla_paused = False
                        ticket.sla_pause_start = False
                        ticket.message_post(
                            body="SLA reanudado por respuesta del cliente.")
                # Si el mensaje es de un empleado, pausar el SLA
                else:
                    if not ticket.sla_paused:
                        ticket.sla_paused = True
                        ticket.sla_pause_start = fields.Datetime.now()
                        ticket.message_post(
                            body="SLA pausado tras mensaje del equipo.")

        return message


class HelpdeskSLAStatus(models.Model):
    _inherit = 'helpdesk.sla.status'

    def _compute_sla_deadline(self):
        # Calcular el plazo del SLA ajustado por el tiempo pausado
        for sla_status in self:
            ticket = sla_status.ticket_id
            sla = sla_status.sla_id
            if not ticket or not sla:
                sla_status.deadline = False
                continue

            # Obtener el tiempo del SLA (en horas)
            sla_time = sla.time if sla.time else sla.time_days * 24.0 if sla.time_days else 0.0
            if not sla_time:
                sla_status.deadline = False
                continue

            # Obtener la fecha de inicio (creación del ticket)
            start_date = ticket.create_date

            # Calcular el tiempo pausado
            if ticket.sla_paused and ticket.sla_pause_start:
                pause_duration = (fields.Datetime.now(
                ) - ticket.sla_pause_start).total_seconds() / 3600.0
                total_paused = ticket.sla_total_paused_time + pause_duration
            else:
                total_paused = ticket.sla_total_paused_time

            # Calcular el deadline base sumando el tiempo del SLA al start_date
            calendar = sla.company_id.resource_calendar_id or self.env.company.resource_calendar_id
            deadline = calendar.plan_hours(
                sla_time, start_date, compute_leaves=True)

            # Ajustar el deadline sumando el tiempo pausado
            if deadline:
                deadline = deadline + timedelta(hours=total_paused)
                sla_status.deadline = deadline
            else:
                sla_status.deadline = False
