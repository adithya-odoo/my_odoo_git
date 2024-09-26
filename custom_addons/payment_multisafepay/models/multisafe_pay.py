# -*- coding: utf-8 -*-

import requests

from odoo import _, fields, models

from odoo.exceptions import ValidationError


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('multisafepay', 'Multisafepay')],
                            ondelete={'multisafepay': 'set default'})
    multisafepay_api_key = fields.Char(
        string="Multisafepay api key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="multisafepay")

    def _multisafepay_make_request(self, data=None, method='POST'):
        print("ftt")
        self.ensure_one()
        # endpoint = f'/v2/{endpoint.strip("/")}'
        url = "https://testapi.multisafepay.com/v1/json/orders?api_key=b175e0dd691f63e653583ac3c6e3b55ab27f0792"

        # odoo_version = service.common.exp_version()['server_version']
        # module_version = self.env.ref(
        #     'base.module_payment_mollie').installed_version
        headers = {
            "Accept": "application/json",
            # "Authorization": f'Bearer {self.mollie_api_key}',
            "Content-Type": "application/json",
            # See https://docs.mollie.com/integration-partners/user-agent-strings
            # "User-Agent": f'Odoo/{odoo_version} MollieNativeOdoo/{module_version}',
        }

        response = requests.request(method, url, json=data, headers=headers)

        print(response.text)
        return response.json()