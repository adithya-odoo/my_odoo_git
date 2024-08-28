from itertools import product

from odoo import Command, models


class SaleOrder(models.Model):
    """ To calculate the sales team  and member commission when clicking the confirm button """
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
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

        if self.team_id.crm_commission_id.type == 'revenue wise':
            if self.team_id.crm_commission_id.revenue_wise == 'straight':
                sum_subtotal = sum(self.order_line.mapped('price_subtotal'))
                for record in self.team_id.crm_commission_id:
                    print(record.to_amount)
                    if record.from_amount <= sum_subtotal < record.to_amount:
                        self.team_id.team_commission_ids = [Command.create({
                            'commission_name': self.team_id.crm_commission_id.name,
                            'sale_amount': sum_subtotal,
                            'rate': record.rate,
                            'commission': record.commission,
                        })]
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

        if self.team_id.crm_commission_id.type == 'product wise':
            sum_amount = 0
            sum_rate = 0
            sales_amount = 0
            order_line = self.order_line
            for rec in order_line:
                print(rec.product_template_id)
                if rec.product_template_id.id == self.team_id.crm_commission_id.product_ids.product_id.id:
                    quantity = rec.product_uom_qty
                    sum_amount += (self.team_id.crm_commission_id.product_ids.max_commission_amount * quantity)
                    sum_rate += self.team_id.crm_commission_id.product_ids.rate_percentage * quantity
                    sales_amount += rec.price_subtotal

            self.team_id.team_commission_ids = [Command.create({
                    'commission_name': self.team_id.crm_commission_id.name,
                    'sale_amount': sales_amount,
                    'commission': sum_rate,
                    'rate': sum_amount,
             })]

        if self.user_id.crm_commission_id.type == 'product wise':
            sum_amount = 0
            sum_rate = 0
            sales_amount = 0
            order_line = self.order_line
            for rec in order_line:
                print(rec.product_template_id)
                if rec.product_template_id.id == self.user_id.crm_commission_id.product_ids.product_id.id:
                    quantity = rec.product_uom_qty
                    sum_amount += self.user_id.crm_commission_id.product_ids.max_commission_amount * quantity
                    sum_rate += self.user_id.crm_commission_id.product_ids.rate_percentage * quantity
                    sales_amount += rec.price_subtotal

            self.user_id.users_commission_ids = [Command.create({
                    'commission_name': self.user_id.crm_commission_id,
                    'sale_amount': sales_amount,
                    'commission': sum_rate,
                    'rate': sum_amount,
                })]

        return res
