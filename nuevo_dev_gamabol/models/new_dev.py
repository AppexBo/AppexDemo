# from odoo import models, fields, api

# class ReportPosOrder(models.Model):
#     _inherit = 'report.pos.order'

#     has_barcode = fields.Boolean(
#         string="¿Tiene código de barras?",
#         compute='_compute_has_barcode',
#         store=False,
#         search='_search_has_barcode'
#     )

#     def _compute_has_barcode(self):
#         for rec in self:
#             rec.has_barcode = False  # No se muestra en pantalla, solo sirve para el filtro

#     @api.model
#     def _search_has_barcode(self, operator, value):
#         # value = True => productos CON código de barras
#         # value = False => productos SIN código de barras
#         product_ids = self.env['product.product'].search([
#             ('barcode', '!=', False) if value else ('barcode', '=', False)
#         ]).ids

#         order_line_ids = self.env['pos.order.line'].search([
#             ('product_id', 'in', product_ids)
#         ]).mapped('order_id.id')

#         return [('order_id', 'in', order_line_ids)]
from odoo import fields, models

class ReportPosOrder(models.Model):
    _inherit = 'report.pos.order'

    barcode = fields.Char(string='Código de Barras', readonly=True)

    def _select(self):
        return f"""
            {super()._select()},
            pp.barcode AS barcode
        """

    def _from(self):
        return f"""
            {super()._from()}
            LEFT JOIN product_product pp ON pp.id = l.product_id
        """

    def _group_by(self):
        return f"""
            {super()._group_by()},
            pp.barcode
        """


