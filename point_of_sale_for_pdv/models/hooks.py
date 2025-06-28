from odoo import api, SUPERUSER_ID

def remove_company_custom_fields(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    field_names = ['state_id', 'province_id', 'municipality_id']
    model_name = 'res.company'

    for field_name in field_names:
        field = env['ir.model.fields'].search([
            ('model', '=', model_name),
            ('name', '=', field_name)
        ])
        if field:
            print(f"🧹 Eliminando campo '{field_name}' del modelo '{model_name}'")
            field.unlink()
