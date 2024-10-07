# controllers/fuel_onboarding.py
# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class FuelOnboardingController(http.Controller):

    @http.route('/fuel_control/fuel_onboarding_panel', auth='user', type='json')
    def fuel_onboarding(self):
        """ Devuelve el banner para el onboarding del control de combustible. """

        return {
            'html': request.env['ir.qweb']._render('fuel_control.fuel_onboarding_panel')
        }