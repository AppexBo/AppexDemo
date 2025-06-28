{
    'name': 'point of sale for pdv',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Nuevo ajuste para los puntos de venta en la facturacion BO',
    'depends': [ 'base',
        'contacts',
        'account',
        'l10n_bo', 
        'base_address_extended'],
    'data':[
        'views/ocultar_campos_res_company.xml',
        'views/nuevo_campos_point_sale.xml'
    ],
  
    'installable': True,
    'application': False,
}
