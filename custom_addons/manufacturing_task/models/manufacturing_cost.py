# -*- coding: utf-8 -*-

import datetime

from odoo import api, Command, fields, models


class ManufacturingCost(models.Model):
    """ To insert cost field and calculate its value"""
    _inherit = "mrp.production"

    component_cost = fields.Float(string="Component Cost", compute="_compute_component_cost", store=True)
    extra_cost_ids = fields.One2many(comodel_name="product.template",
                                  relation='product_manufacturing_rel',
                                  string="Extra cost")
    invoice_id = fields.Many2one('account.move', string="Invoice",
                                 store=True)

    @api.depends('move_raw_ids')
    def _compute_component_cost(self):
        """To compute the Component Cost"""
        print(self.move_raw_ids)
        component_cost = 0
        for line in self.move_raw_ids:
            component_cost += line.product_tmpl_id.standard_price
        self.component_cost = component_cost

    def action_create_invoice(self):
        """ To create Bill"""
        bill_vals = []
        for record in self.move_raw_ids:
            if record.picked:
                bill_vals.append(
                    Command.create({'product_id': record.product_id.id,
                                     'quantity': record.quantity,
                                }))
        # for record in self.extra_cost_ids:
        #      bill_vals.append(
        #      Command.create({'product_id': record.name,
        #                      'quantity': record.standard_price,
        #                         }))

        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'date': datetime.date.today(),
            'invoice_date': datetime.date.today(),
            'invoice_line_ids': bill_vals
        })
        self.invoice_id = bill.id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Vendor Bill',
            'res_model': 'account.move',
            'res_id': bill.id,
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
        }
        # Vendor Bill



