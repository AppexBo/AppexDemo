import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    #def update_selected_stock_pickings(self):
    #    for order in self:
    #        for element in order.move_ids_without_package:
    #            #_logger.info(element)
    #            try:
    #                # quantity es la cantidad y la demanda es product_uom_qty
    #                element.write({
    #                    'quantity': element.product_uom_qty  # Asigna el valor de product_uom_qty a quantity
    #                })
    #            except Exception as e:
    #                _logger.error(f"Error al actualizar el elemento {element}: {str(e)}")
    #                break  
    #    #log informativo que se actualizo lo seleccionado
    #    _logger.info("Se actualizaron todos los stocks seleccionados")
    #    # Recargar la vista
    #    return {
    #        'type': 'ir.actions.client',
    #        'tag': 'reload',
    #    }

    #@api.model
    
    #def write(self, vals):
    #    if len(self) == 1:
    #        for field_name in self._fields:
    #            field_value = getattr(self, field_name, 'No disponible')
    #            #aqui lo que hago es obtener el campo products_availability_state y valido si dice que esta disponible la cantidad osea que diga available
    #            if field_name == "products_availability_state" and field_value == "available":  
    #                #caso que si haya que automatice a finalizado
    #                self.button_validate()
    #                #vals["state"] = "done"
    #    res = super(StockPicking, self).write(vals)
    #    return res

    @api.model
    def write(self, vals):
        if len(self) == 1:
            availability_state = getattr(self, "products_availability_state", False)
            
            if availability_state == "available":
                # Caso 1: Ya está disponible - validar directamente
                self.button_validate()
            else:
                # Caso 2: No está disponible - actualizar cantidades y luego validar
                # Primero actualizamos las cantidades
                for element in self.move_ids_without_package:
                    try:
                        element.write({
                            'quantity': element.product_uom_qty
                        })
                    except Exception as e:
                        _logger.error(f"Error al actualizar el elemento {element}: {str(e)}")
                
                # Verificamos nuevamente la disponibilidad después de actualizar
                updated_availability = getattr(self, "products_availability_state", False)
                if updated_availability == "available":
                    self.button_validate()
        
        return super(StockPicking, self).write(vals)