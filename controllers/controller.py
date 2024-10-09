from odoo import http
from odoo.http import request
import json
from odoo.exceptions import UserError 

class FuelOnboardingController(http.Controller):
    @http.route('/fuel_control/fuel_onboarding_panel', auth='user', type='json')
    def fuel_onboarding(self):
        records = request.env['fuel.control'].search([], order='create_date desc', limit=1)
        if records:
            total = records.total
        else:
            total = 0        
        return {
        'html': request.env['ir.qweb']._render('fuel_control.fuel_onboarding_panel', {'total': total})
        }

    @http.route('/fuel_control/fuel_onboarding_panel_dates', auth='user', type='http', methods=['POST'], csrf=False)
    def fuel_onboarding_dates(self, **kwargs):
        date_from = kwargs.get('date_from')
        date_to = kwargs.get('date_to')
        
        if not date_from or not date_to:
            return request.redirect('/web#action=fuel_control.action_fuel_control_tree&error=Fechas no pueden estar vacías')
        
        try:
            request.env['fuel.control'].set_fechas(date_from, date_to)
        except Exception as e:
            raise UserError(f"Error al guardar las fechas: {str(e)}")

        # Redirigir a la acción predefinida con el dominio aplicado y codificado
        return request.redirect(f'/web#action=fuel_control.action_open_fuel_control')
        