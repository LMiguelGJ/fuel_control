# -*- coding: utf-8 -*-

# models/fuel_control.py
from odoo import models, fields, api

class FuelControl(models.Model):
    _name = 'fuel.control'
    _description = 'Control de Combustible'
    _order = 'date desc'

    date = fields.Date(string='Fecha')
    
    received_by = fields.Char(string="Recibido por")
    
    quantity_in = fields.Float(string='Cantidad Entrante', default=False)
    
    quantity_out = fields.Float(string='Cantidad Saliente', default=False)
    
    total = fields.Float(string='Total Actual',
                         compute='_compute_total', store=True)
    
    date_from = fields.Date(string='Desde')
    date_to = fields.Date(string='Hasta')

    @api.onchange('date_from', 'date_to')
    def _onchange_dates(self):
        if self.date_from and self.date_to:
            return {
                        'type': 'ir.actions.act_window',
                        'name': 'Ver Transacciones',
                        'res_model': 'fuel.control',
                        'view_mode': 'tree',
                        'view_id': self.env.ref('fuel_control.view_fuel_control_tree').id,
                        'domain': [('date', '>=', self.date_from), ('date', '<=', self.date_to)],
                        'context': self.env.context,
                    }
    
    @api.model
    def default_get(self, fields):
        res = super(FuelControl, self).default_get(fields)
        self.remove_empty_date_records_and_return_action()
        return res

    def remove_empty_date_records_and_return_action(self):
        records_to_delete = self.search([('date', '=', False)])
        records_to_delete.unlink()
    
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
