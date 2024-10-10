# -*- coding: utf-8 -*-

# models/fuel_control.py
from odoo import models, fields, api


class FuelControl(models.Model):
    _name = 'fuel.control'
    _description = 'Control de Combustible'
    _order = 'date desc'

    date = fields.Date(string='Fecha')
  
    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, default='Nuevo')

    received_by = fields.Char(string="Recibido por")
    
    quantity_in = fields.Float(string='Cantidad Entrante', default=False)
    
    quantity_out = fields.Float(string='Cantidad Saliente', default=False)
    
    total = fields.Float(string='Total Actual',
                         compute='_compute_total', store=True)
    
    @api.model
    def action_open_fuel_control(self):
        action = self.env.ref('fuel_control.action_fuel_control_tree').read()[0]
        
        # Obtener las fechas de los parámetros del sistema
        fecha_inicio = self.env['ir.config_parameter'].get_param('fuel.control.fecha_inicio')
        fecha_fin = self.env['ir.config_parameter'].get_param('fuel.control.fecha_fin')
        
        # Validar que las fechas no estén vacías
        if fecha_inicio and fecha_fin:
            action['domain'] = [('date', '>=', fecha_inicio), ('date', '<=', fecha_fin)]
        else:
            action['domain'] = []

        return action
    
    @api.model
    def set_fechas(self, fecha_inicio, fecha_fin):
        # Guardar las fechas en los parámetros del sistema
        params_to_delete = self.env['ir.config_parameter'].search([
            ('key', 'in', ['fuel.control.fecha_inicio', 'fuel.control.fecha_fin'])
        ])
        
        if params_to_delete:
            params_to_delete.unlink()

        self.env['ir.config_parameter'].set_param('fuel.control.fecha_inicio', fecha_inicio)
        self.env['ir.config_parameter'].set_param('fuel.control.fecha_fin', fecha_fin)

    @api.model
    def delete_fechas(self):
        action = self.env.ref('fuel_control.action_fuel_control_tree').read()[0]

        # Guardar las fechas en los parámetros del sistema
        params_to_delete = self.env['ir.config_parameter'].search([
            ('key', 'in', ['fuel.control.fecha_inicio', 'fuel.control.fecha_fin'])
        ])
        
        if params_to_delete:
            params_to_delete.unlink()
        
        return action

    
    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('fuel.control') or '/'
        return super().create(vals_list)
    
    
    @api.model
    def remove_empty_date_records_and_return_action(self):
        records_to_delete = self.search([('date', '=', False)])
        if records_to_delete:
            records_to_delete.unlink()
        # Retorna la acción para abrir la vista tree
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fuel Control Tree View',
            'view_mode': 'tree',
            'res_model': 'fuel.control',
            'target': 'current',
        }
    
    @api.depends('quantity_in', 'quantity_out')
    def _compute_total(self):
        for record in self:
            # Calcular el total acumulado a partir de todos los registros
            total_quantity_in = sum(rec.quantity_in for rec in self.search([]))
            total_quantity_out = sum(rec.quantity_out for rec in self.search([]))
            record.total = total_quantity_in - total_quantity_out
            
    def action_open_wizard_in(self):
        return {
            'name': 'Depositar Combustible',
            'type': 'ir.actions.act_window',
            'res_model': 'fuel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'action': 'in', 'active_id': self.id},
        }

    def action_open_wizard_out(self):
        return {
            'name': 'Retirar Combustible',
            'type': 'ir.actions.act_window',
            'res_model': 'fuel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'action': 'out', 'active_id': self.id},
        }
