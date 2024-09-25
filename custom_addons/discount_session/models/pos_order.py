# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosOrder(models.Model):
    """to add a field and to send total discount to pos"""
    _inherit = 'pos.order'

    total_discount_amount = fields.Float(string="Total Discount Amount", compute="_compute_session_discount_amount")
    # whole_total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount")

    @api.depends('lines')
    def _compute_session_discount_amount(self):
        """Computes total discount amount of the order"""
        for rec in self:
            total_discount_amount = 0
            for records in rec.lines:
                total_discount_amount += records.discount_amount
                rec.total_discount_amount = total_discount_amount

    @api.model
    def return_total_discount_pos(self, pos_session_id):
        """sends the total discount amount of all orders in currently opened session to pos"""
        records = self.search([('session_id', '=', pos_session_id)])
        total_discount = 0
        for rec in records:
            total_discount += rec.total_discount_amount
        return total_discount

    @api.depends('lines')
    def _compute_total_amount(self):
        total_amount = 0
        for rec in self:
            for record in rec.lines:
                total_amount += record.total_price
                rec.whole_total_amount = total_amount
        return total_amount

    @api.model
    def return_total_pos_amount(self, pos_session_id):
        """sends the total discount amount of all orders in currently opened session to pos"""
        records = self.search([])
        total_amount = 0
        for rec in records:
            total_amount += rec.whole_total_amount
        return total_amount



