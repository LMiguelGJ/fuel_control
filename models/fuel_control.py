# -*- coding: utf-8 -*-

# models/fuel_control.py
from odoo import models, fields, api
from datetime import date, timedelta


class FuelControl(models.Model):
    _name = 'fuel.control'
    _description = 'Control de Combustible'
    _order = 'date desc'

    date = fields.Date(string='Fecha')
    
    date_to = fields.Date(string='Fecha', default=lambda self: date.today())
    
    date_from = fields.Date(string='Fecha', default=lambda self: date.today() - timedelta(days=7))
  
    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, default='Nuevo')

    received_by = fields.Char(string="Recibido por")
    
    quantity_in = fields.Float(string='Cantidad Entrante', default=False)
    
    quantity_out = fields.Float(string='Cantidad Saliente', default=False)
    
    total = fields.Float(string='Total Actual',
                         compute='_compute_total', store=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('fuel.control') or '/'
        return super(FuelControl, self).create(vals)

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
