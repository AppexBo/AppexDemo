{
    'name': 'SLA Custom, APPEX BOLIVIA',
    'version': '1.0',
    'category': '',
    'description':'By for Appex',
    'summary': 'SLA',
    'depends': ['helpdesk'],
    'assets': {
        'point_of_sale._assets_pos': [
            'recibo_punto_venta/static/src/xml/custom_receipt.xml',
        ],
    },
  
    'installable': True,
    'application': False,
}
