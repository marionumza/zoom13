
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



class inheritEventType(models.Model):

    _inherit = ["event.type"]

    # location
    is_online = fields.Boolean(
        'Online Event', help='Online events like webinars do not require a specific location and are hosted online.')

class inheritEvent(models.Model):

    _inherit = ["event.event"]

    is_online = fields.Boolean('Online Event')
    twitter_hashtag = fields.Char('Twitter Hashtag')

    def button_draft(self):
        self.write({'stage_id': 'draft'})
    def button_cancel(self):
        if any('done' in event.mapped('registration_ids.state') for event in self):
            raise UserError(_("There are already attendees who attended this event. Please reset it to draft if you want to cancel this event."))
        self.registration_ids.write({'stage_id': 'cancel'})
        self.state = 'cancel'
    def button_done(self):
        self.write({'stage_id': 'done'})
    def button_confirm(self):
        self.write({'stage_id': 'confirm'})


    @api.model
    def _is_event_registrable(self):
        return True
    #--------------------------------------------

    meeting_type = fields.Selection(
        string='Meeting Type',
        selection=[
       
        ]
    )
    meeting_id = fields.Char(
        string='Meeting Id')
    
    moderator_password = fields.Char(
        string='Moderator Password')
    
    attendies_password = fields.Char(
        string='Attendee Password')
    
    temp_key = fields.Char(
        string='temp_key',
        store=True)

    public_url = fields.Char(string="public_url", default="Class Not Initiated")
    moderator_url = fields.Char(string='Moderator Url')

    @api.onchange('event_type_id')
    def _onchange_type(self):
        # super(inheritEvent, self)._onchange_type()
        if self.event_type_id.is_online:
            print (">>>>>>>>>>>>>>>>>>>>>>>>>")
            self.is_online = True

    def button_cancel(self):

        self.is_meeting_active = False
        for registration_ids in self.registration_ids:
            registration_ids.is_active = False                 

        res = super(inheritEvent, self).button_cancel()


    is_meeting_active = fields.Boolean(
        string='Meeting Initiated',        
        default=False,
        readonly=True,
        store=True)

    def initiate_class(self):
        for rec in self:
            if self.meeting_type == False:
                raise ValidationError(_("Please Select Type before Initiating Meeting"))  
            print ("/////////////////first base class")
            pass

 