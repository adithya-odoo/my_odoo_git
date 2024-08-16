# -*- coding: utf-8 -*-

from odoo import fields, models


class RepairTag(models.Model):
    _name = "repair.tag"
    _description = "Repair tag"

    name = fields.Char(string="Name")
    color = fields.Integer(string="Color")

