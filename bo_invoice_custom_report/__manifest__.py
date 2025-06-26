{
    'name': 'Personalización de Reporte Boliviano 18',
    'version': '17.0.1.0.0',
    'summary': 'Personaliza el reporte fiscal boliviano de l10n_bo',
    'author': 'Tu Nombre',
    'depends': ['account','l10n_bo_bolivian_invoice'],
    'data': [
        'views/paper_format.xml',
        'views/report_roll_inherit.xml',
        
        'views/boton.xml',
        'views/cuerpo.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
