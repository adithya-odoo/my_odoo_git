# -*- coding: utf-8 -*-

from odoo import fields, models


class CrmLead(models.Model):
    """crm inherited model"""
    _inherit = 'crm.team'

    crm_stage_id = fields.Many2one('crm.stage', string='Stage')
