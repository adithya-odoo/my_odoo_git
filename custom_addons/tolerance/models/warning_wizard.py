# -*- coding: utf-8 -*-

from odoo import fields, models


class WarningWizard(models.TransientModel):
   """This model is used to send warning message."""
   _name = 'warning.wizard'
   _description = "Warning Wizard"

   tolerance = fields.Float(string="Tolerance", readonly=True)

   def action_accept(self):
      """ Accept the delivery through wizard """
      pick_id = self.env.context.get('active_id')
      self.env['stock.picking'].browse(pick_id).write({
         'state' : 'done'
      })

   def action_reject(self):
      """ Reject the delivery through wizard """
      pick_id = self.env.context.get('active_id')
      self.env['stock.picking'].browse(pick_id).write({
         'state' : 'cancel'
      })


