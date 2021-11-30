
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################



from odoo import models, fields, api
import requests
import json
from odoo import api, models, _
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_is_zero
import ast
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)



class inheritEventeLearning(models.Model):
    _inherit = ["event.event"]

  
  

    slide_channel_id = fields.Many2one(
        string="Slide Channel", comodel_name="slide.channel",
    )

    is_elearning_event = fields.Boolean(
        string='is_elearnig_event',        
        default=False,
        store=True         
    )

    def initiate_elearning_class_event(self):
        for rec in self:
            print ("func of eLearning base module : name// initiate_elearning_class_event")
            pass

    def button_confirm(self):
        res = super(inheritEventeLearning, self).button_confirm()
        existing_parcipitants = self.registration_ids.mapped('partner_id')

        if self.is_elearning_event:
            for partners in self.slide_channel_id.channel_partner_ids:         
                new_attendy = self.env['event.registration'].create({'partner_id':partners.partner_id.id,'event_id': self.id})

        self.is_published = True
    




    @api.onchange('slide_channel_id')
    def _onchange_field(self):
        for rec in self:
            rec.user_id = rec.slide_channel_id.user_id



