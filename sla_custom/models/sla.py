from odoo import models, fields, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sla_paused = fields.Boolean(string="SLA Pausado", default=True)
    sla_pause_start = fields.Datetime(string="Inicio de Pausa del SLA")
    sla_total_paused_time = fields.Float(string="Tiempo Total Pausado (Horas)", default=0.0)

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
                ticket.sla_ids._compute_deadline()
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
                            pause_duration = (fields.Datetime.now() - pause_start).total_seconds() / 3600.0
                            ticket.sla_total_paused_time += pause_duration
                        ticket.sla_paused = False
                        ticket.sla_pause_start = False
                # Si el mensaje es de un empleado, pausar el SLA
                else:
                    if not ticket.sla_paused:
                        ticket.sla_paused = True
                        ticket.sla_pause_start = fields.Datetime.now()
                        
        return message

class HelpdeskSLA(models.Model):
    _inherit = 'helpdesk.sla'

    def _compute_deadline(self):
        # Sobrescribir el cálculo del plazo del SLA
        for sla in self:
            ticket = sla.ticket_id
            if ticket.sla_paused and ticket.sla_pause_start:
                # Excluir el tiempo pausado actual
                pause_duration = (fields.Datetime.now() - ticket.sla_pause_start).total_seconds() / 3600.0
                total_paused = ticket.sla_total_paused_time + pause_duration
            else:
                total_paused = ticket.sla_total_paused_time

            # Ajustar el deadline restando el tiempo pausado
            original_deadline = super(HelpdeskSLA, sla)._compute_deadline()
            if original_deadline:
                sla.deadline = fields.Datetime.from_string(original_deadline) + timedelta(hours=total_paused)