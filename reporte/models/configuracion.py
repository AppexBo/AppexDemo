from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from num2words import num2words


class Configuracion(models.Model):
    _inherit = 'account.move'

    terms_and_conditions = fields.Text(
        'Términos y condiciones')  # Aquí agregamos el campo
    razon_social_micelaneo_id = fields.Many2one(
        comodel_name='res.partner', string='Razón Social', store=True)

    def number_to_word(self, number: float):
        decimal_part = int(round(number % 1, 2) * 100)
        integer_part = int(number)
        # get actual language
        lang = self.env.context.get('lang', 'es_ES')
        return f"{num2words(integer_part, lang=lang)} con {decimal_part}/100 {self.currency_id.symbol}"
    codigo_A1_or_A2 = fields.Char(
        string='Código A1 o A2',
        compute='_compute_codigo_fiscal',
        store=False
    )

    @api.depends('company_id.company_registry')
    def _compute_codigo_fiscal(self):
        for record in self:
            if record.company_id.company_registry == '100':
                record.codigo_A1_or_A2 = "A1"
            elif record.company_id.company_registry == '200':
                record.codigo_A1_or_A2 = "A2"
            else:
                record.codigo_A1_or_A2 = ""

    mes_secuencia = fields.Char(
        string="Secuencia por Mes", compute='_compute_mes_secuencia', store=True)

    @api.depends('date', 'journal_id', 'state')
    def _compute_mes_secuencia(self):
        for record in self:
            if record.date and record.journal_id:
                # Obtener mes y año
                mes = record.date.strftime('%m')
                start_of_month = record.date.replace(day=1)
                end_of_month = start_of_month + relativedelta(months=1)

                # Buscar movimientos del mismo diario y mismo mes
                domain = [
                    ('date', '>=', start_of_month),
                    ('date', '<', end_of_month),
                    ('journal_id', '=', record.journal_id.id),
                    ('state', '=', record.state),
                    # Excluir borradores si quieres solo facturas confirmadas:
                    # ('state', '!=', 'draft')
                ]

                # Obtener movimientos ordenados por fecha y por ID (para evitar colisiones en el mismo día)
                moves = self.env['account.move'].search(
                    domain, order='date asc, id asc')

                # Generar secuencia incremental
                for idx, move in enumerate(moves, start=1):
                    secuencial = f"{idx:05d}"
                    mes_str = move.date.strftime('%m')
                    move.mes_secuencia = f"-{mes_str}-{secuencial}"
            else:
                record.mes_secuencia = ''
    # @api.depends('date', 'journal_id', 'journal_id.type')
    # def _compute_mes_secuencia(self):
    #     for record in self:
    #         if record.date and record.journal_id and record.journal_id.type:
    #             # Extraer el mes en formato 'MM' (ej. '03' para marzo)
    #             mes = record.date.strftime('%m')
    #             # Definir el rango del mes actual
    #             start_of_month = record.date.replace(day=1)
    #             end_of_month = start_of_month + relativedelta(months=1)

    #             # Dominio para contar movimientos en el mismo mes y tipo de diario
    #             domain = [
    #                 ('date', '>=', start_of_month),
    #                 ('date', '<', end_of_month),
    #                 ('journal_id.type', '=', record.journal_id.type),  # Filtrar por tipo de diario
    #             ]
    #             # Excluir el registro actual si ya existe
    #             if record.id:
    #                 domain.append(('id', '!=', record.id))

    #             # Contar los movimientos previos en este mes y tipo de diario, y sumar 1
    #             ultimo_numero = self.env['account.move'].search_count(domain) + 1
    #             secuencial = f"{ultimo_numero:05d}"  # Formato '00001', '00002', etc.
    #             record.mes_secuencia = f"-{mes}-{secuencial}"
    #         else:
    #             record.mes_secuencia = ''

    @api.model
    def create(self, vals):
        record = super(Configuracion, self).create(vals)
        record._compute_mes_secuencia()  # Asegurar que se calcule al crear
        return record
