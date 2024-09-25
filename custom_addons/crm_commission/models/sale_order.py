# -*- coding: utf-8 -*-

from odoo import Command, models


class SaleOrder(models.Model):
    """ To calculate the sales team  and member commission when clicking the confirm button """
    _inherit = 'sale.order'

    def action_confirm(self):
        """ To create a commission percentage inside the sale team and salesperson
         while clicking the confirm button inside the sale order (if the commission
         set inside the sale team/salesperson)"""
        res = super().action_confirm()

        """ if the commission inside the sale team is 'revenue' and 'graduated' """
        if self.team_id.crm_commission_id.type == 'revenue wise':
            if self.team_id.crm_commission_id.revenue_wise == 'graduated':
                sum_subtotal = sum(self.order_line.mapped('price_subtotal'))
                for record in self.team_id.crm_commission_id.graduated_ids:
                    if record.from_amount <= sum_subtotal < record.to_amount:
                        self.team_id.team_commission_ids = [Command.create({
                            'commission_name': self.team_id.crm_commission_id.name,
                            'sale_amount': sum_subtotal,
                            'rate': record.rate,
                            'commission': record.commission,
                        })]

        """ if the commission inside the salesperson is 'revenue' and 'graduated'"""
        if self.user_id.crm_commission_id.type == 'revenue wise':
            if self.user_id.crm_commission_id.revenue_wise == 'graduated':
                sum_subtotal = sum(self.order_line.mapped('price_subtotal'))
                for record in self.user_id.crm_commission_id.graduated_ids:
                    if record.from_amount <= sum_subtotal < record.to_amount:
                        self.user_id.users_commission_ids = [Command.create({
                            'commission_name': self.user_id.crm_commission_id.name,
                            'sale_amount': sum_subtotal,
                            'rate': record.rate,
                            'commission': record.commission,
                        })]

        """if the commission inside the sale team is 'revenue' and 'straight'"""
        if self.team_id.crm_commission_id.type == 'revenue wise':
            if self.team_id.crm_commission_id.revenue_wise == 'straight':
                sum_subtotal = sum(self.order_line.mapped('price_subtotal'))
                for record in self.team_id.crm_commission_id:
                    if record.from_amount <= sum_subtotal < record.to_amount:
                        self.team_id.team_commission_ids = [Command.create({
                            'commission_name': self.team_id.crm_commission_id.name,
                            'sale_amount': sum_subtotal,
                            'rate': record.rate,
                            'commission': record.commission,
                        })]

        """if the commission inside the salesperson is 'revenue' and 'straight'"""
        if self.user_id.crm_commission_id.type == 'revenue wise':
            if self.user_id.crm_commission_id.revenue_wise == 'straight':
                sum_subtotal = sum(self.order_line.mapped('price_subtotal'))
                for record in self.user_id.crm_commission_id:
                    if record.from_amount <= sum_subtotal < record.to_amount:
                        self.user_id.users_commission_ids = [Command.create({
                            'commission_name': self.user_id.crm_commission_id.name,
                            'sale_amount': sum_subtotal,
                            'rate': record.rate,
                            'commission': record.commission,
                        })]

        """if the commission inside the sale team is 'product wise'"""
        if self.team_id.crm_commission_id.type == 'product wise':
            sum_amount = 0
            sum_rate = 0
            sales_amount = 0
            is_true = False
            order_line = self.order_line
            for rec in order_line:
                for record in self.team_id.crm_commission_id.product_ids:
                    if rec.product_template_id.id == record.product_id.id:
                        is_true = True
                        quantity = rec.product_uom_qty
                        sum_amount += record.max_commission_amount * quantity
                        sum_rate += record.rate_percentage * quantity
                        sales_amount += rec.price_subtotal
            if is_true:
                self.team_id.team_commission_ids = [Command.create({
                    'commission_name': self.team_id.crm_commission_id.name,
                    'sale_amount': sales_amount,
                    'commission': sum_rate,
                    'rate': sum_amount,
                  })]

        """if the commission inside the salesperson is 'product wise'"""
        if self.user_id.crm_commission_id.type == 'product wise':
            sum_amount = 0
            sum_rate = 0
            sales_amount = 0
            is_true = False
            order_line = self.order_line
            for rec in order_line:
                for record in self.user_id.crm_commission_id.product_ids:
                    if rec.product_template_id.id == record.product_id.id:
                        is_true = True
                        quantity = rec.product_uom_qty
                        sum_amount += record.max_commission_amount * quantity
                        sum_rate += record.rate_percentage * quantity
                        sales_amount += rec.price_subtotal
            if is_true:
                self.user_id.users_commission_ids = [Command.create({
                    'commission_name': self.user_id.crm_commission_id,
                    'sale_amount': sales_amount,
                    'commission': sum_rate,
                    'rate': sum_amount,
                })]

        return res
