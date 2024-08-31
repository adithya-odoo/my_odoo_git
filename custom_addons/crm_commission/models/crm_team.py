# -*- coding: utf-8 -*-

from odoo import fields, models


class CrmTeam(models.Model):
    """ To insert crm commission field inside sales team """
    _inherit = 'crm.team'

    crm_commission_id = fields.Many2one(comodel_name='crm.commission',
                                        string="Commission")
    team_commission_ids = fields.One2many(comodel_name='team.commission',
                                          inverse_name='team_commission_id',
                                          string="Team commission")