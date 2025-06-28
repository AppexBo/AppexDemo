from odoo import api, SUPERUSER_ID

def remove_custom_fields(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    model_name = 'res.company'
    fields_to_remove = ['state_id', 'province_id', 'municipality_id']

    for field_name in fields_to_remove:
        field = env['ir.model.fields'].search([
            ('model', '=', model_name),
            ('name', '=', field_name)
        ])
        if field:
            field.unlink()
