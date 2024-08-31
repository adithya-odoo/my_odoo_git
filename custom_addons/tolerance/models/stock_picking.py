# -*- coding: utf-8 -*-

from odoo import models


class SalePicking(models.Model):
    """ To pop up the wizard if the quantity is not between lower_limit and
     higher limit """
    _inherit = 'stock.picking'

    def button_validate(self):
        """ Lower limit and higher limit will calculate automatically when clicking
        the validate button in delivery page and also pop up the wizard if the
         quantity is not between lower_limit and higher limit """
        res = super().button_validate()
        sale_order = self.env['sale.order'].search([('name', '=', self.origin)])
        if sale_order:
            for line in sale_order.order_line:
                lower_quantity = (line.product_uom_qty
                                  - int(line.tolerance * 100))
                upper_quantity = (line.product_uom_qty
                              + int(line.tolerance * 100))

            for record in self.move_ids_without_package:
                if record.quantity < lower_quantity or record.quantity > upper_quantity:
                    sale_order = self.env['sale.order'].search(
                        [('name', '=', self.origin)])
                    for line in sale_order.order_line:
                        tolerance = line.tolerance

                    return {'type': 'ir.actions.act_window',
                            'name': 'Delivery Warning',
                            'res_model': 'warning.wizard',
                            'target': 'new',
                            'view_mode': 'form',
                            'view_type': 'form',
                            'context': {'default_tolerance': tolerance}

                            }

        purchase_order = self.env['purchase.order'].search([('name', '=', self.origin)])
        if purchase_order:
            for line in purchase_order.order_line:
                lower_quantity = (line.product_uom_qty
                                  - int(line.tolerance * 100))
                upper_quantity = (line.product_uom_qty
                              + int(line.tolerance * 100))

            for record in self.move_ids_without_package:
                if record.quantity < lower_quantity or record.quantity > upper_quantity:
                    purchase_order = self.env['purchase.order'].search(
                                            [('name', '=', self.origin)])
                    for line in purchase_order.order_line:
                        tolerance = line.tolerance
                    return {'type': 'ir.actions.act_window',
                            'name': 'Delivery Warning',
                            'res_model': 'warning.wizard',
                            'target': 'new',
                            'view_mode': 'form',
                            'view_type': 'form',
                            'context': {'default_tolerance': tolerance}
                            }
        return res
