
# from odoo import fields, models

# class ReportPosOrder(models.Model):
#     _inherit = 'report.pos.order'

#     barcode = fields.Char(string='Código de Barras', readonly=True)

#     def _select(self):
#         return f"""
#             {super()._select()},
#             pp.barcode AS barcode
#         """

#     def _from(self):
#         return f"""
#             {super()._from()}
#             LEFT JOIN product_product pp ON pp.id = l.product_id
#         """

#     def _group_by(self):
#         return f"""
#             {super()._group_by()},
#             pp.barcode
#         """

from odoo import models, fields

class ReportPosOrder(models.Model):
    _inherit = 'report.pos.order'

    product_categ_id = fields.Many2one('product.category', string='Categoría del producto', readonly=True)

    def _select(self):
        return f"""
            {super()._select()},
            pt.categ_id AS product_categ_id
        """

    def _from(self):
        return f"""
            {super()._from()}
            LEFT JOIN product_product pp ON pp.id = l.product_id
            LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
        """

    def _group_by(self):
        return f"""
            {super()._group_by()},
            pt.categ_id
        """
