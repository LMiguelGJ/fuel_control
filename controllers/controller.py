from odoo import http
from odoo.http import request
import json

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
        
        domain = [('date', '&gt;=', date_from), ('date', '&lt;=', date_to)]

        # Serializar el dominio como JSON para que sea correctamente codificado en la URL
        domain_json = json.dumps(domain)

        # Redirigir a la acción predefinida con el dominio aplicado y codificado
        return request.redirect(f'/web#action=fuel_control.action_fuel_control_tree&view_type=tree&domain={domain_json}')
        