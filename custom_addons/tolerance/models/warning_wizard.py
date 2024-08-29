# -*- coding: utf-8 -*-

from odoo import fields, models, _


class WarningWizard(models.TransientModel):
   """This model is used to send warning message."""
   _name = 'warning.wizard'
   _description = "Warning Wizard"
   user_id = fields.Many2one('res.partner', string="Recipient")
   tolerance = fields.Float(related=user_id.tolerance)

   # def action_send_msg(self):
   #     """This function is called when
   #      . It opens a
   #       new wizard for warning"""
   #     return {'type': 'ir.actions.act_window',
   #             'name': _('Whatsapp Message'),
   #             'res_model': 'warning.wizard',
   #             'target': 'new',
   #             'view_mode': 'form',
   #             'view_type': 'form',
   #             'context': {'default_user_id': self.id}, }