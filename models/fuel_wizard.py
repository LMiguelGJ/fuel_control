# -*- coding: utf-8 -*-

# models/fuel_wizard.py
from odoo import models, fields, api
from odoo.exceptions import UserError 

class FuelWizard(models.TransientModel):
    _name = 'fuel.wizard'
    _description = 'Wizard para Control de Combustible'

    moment = fields.Date(string='Momento')
    
    received = fields.Char(string="Recibido")
    
    quantity = fields.Float("Cantidad", default=False)
    
    @api.model
    def action_cancel(self, context=None):  

        fuel_control_id = self._context.get('active_id')
        if fuel_control_id:
            fuel_control = self.env['fuel.control'].browse(fuel_control_id)
            fuel_control.unlink()

        return {
            'name': 'Control de Combustible',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'fuel.control',
            'type': 'ir.actions.act_window',
            'target': 'current', 
            'context': self.env.context,
        }
    
    def action_confirm(self):
        # Obtener el registro del control de combustible
        fuel_control = self.env['fuel.control'].browse(self._context.get('active_id'))

        # Validación de los campos
        if not self.moment:
            raise UserError("Por favor, complete el campo 'Fecha' antes de continuar.")
        if 'action' in self._context and self._context['action'] == 'out':
            raise UserError("Por favor, complete el campo 'Recibido por' antes de continuar.")
        if not self.quantity:
            raise UserError("Por favor, complete el campo 'Cantidad' antes de continuar.")

        # Lógica para añadir o retirar combustible
        if 'action' in self._context and self._context['action'] == 'in':
            fuel_control.quantity_in += self.quantity
            fuel_control.date = self.moment
            fuel_control.received_by = self.received

        elif 'action' in self._context and self._context['action'] == 'out':
            fuel_control.quantity_out += self.quantity
            fuel_control.date = self.moment
            fuel_control.received_by = self.received
            
        # Actualizar el total
        fuel_control._compute_total()
        # fuel_control.customLogs(self.received, self.moment, self.quantity)

        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Control de Combustible',
            'res_model': 'fuel.control',
            'view_mode': 'tree',
            'target': 'current',
        }