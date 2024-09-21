from odoo import models, api

class DemoDemo(models.Model):
    _name = "demo.demo"

    @api.model
    def fetch_sales(self):
        print("helooooooooooo")
        return self.env['sale.order'].search([], limit=10)