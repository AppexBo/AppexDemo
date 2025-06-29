from odoo import models, fields

class GestorPermiso(models.Model):
    _name = 'gestor.permiso'
    _description = 'Permiso por Modelo'

    rol_id = fields.Many2one('gestor.rol', string='Rol', required=True)
    modelo_id = fields.Many2one('ir.model', string='Modelo', required=True)

    perm_read = fields.Boolean('Leer')
    perm_write = fields.Boolean('Escribir')
    perm_create = fields.Boolean('Crear')
    perm_unlink = fields.Boolean('Eliminar')