import datetime

from odoo import models, fields

class EventManagement(models.Model):
    _name = "event.management"
    _description = "event management"

    name = fields.Char(required=True)
    expected_price = fields.Float()
    selling_price = fields.Integer(readonly=True, copy=False)
    bedroom = fields.Integer(default=2)
    availablity_date = fields.Datetime(default=fields.Datetime.now())
    active = fields.Boolean()
    status = fields.Selection([('new', 'New'), ('offer Received', 'Offer Received'), ('offer Accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'cancelled')], default='new')
    description = fields.Text()