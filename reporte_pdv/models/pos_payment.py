from odoo import models, fields

class PosPayment(models.Model):
    _inherit = 'pos.payment'

    # En tu modelo pos.payment (pos_payment.py)
    cashier_id = fields.Many2one(
        'hr.employee',
        string='Cajero',
        related='pos_order_id.employee_id',
        readonly=True,
        store=False
    )

    payment_method_name = fields.Char(
        string='Pago',
        compute='_compute_payment_method_name',
        store=True,
    )

    def _compute_payment_method_name(self):
        for payment in self:
            payment.payment_method_name = payment.payment_method_id.name or ''