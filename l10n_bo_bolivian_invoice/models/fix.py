
from odoo import models,fields

class Fix(models.Model):
    _inherit = 'account.move'

    def _stock_account_anglo_saxon_reconcile_valuation(self):
        # Evitar conciliación si algún asiento no está publicado
        draft_moves = self.filtered(lambda m: m.state != 'posted')
        if draft_moves:
            _logger.warning(
                "Se omitió la conciliación porque hay movimientos en borrador.")
            return
        return super()._stock_account_anglo_saxon_reconcile_valuation()
