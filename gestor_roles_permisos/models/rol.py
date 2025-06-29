from odoo import models, fields

class GestorRol(models.Model):
    _name = 'gestor.rol'
    _description = 'Rol Personalizado'

    name = fields.Char('Nombre del Rol', required=True)
    descripcion = fields.Text('Descripción')
    usuario_ids = fields.Many2many('res.users', string="Usuarios")
    permiso_ids = fields.One2many('gestor.permiso', 'rol_id', string="Permisos")