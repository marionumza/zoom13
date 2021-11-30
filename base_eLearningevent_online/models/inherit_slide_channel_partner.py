
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

class inheritslidechannelpartner(models.Model):
    _inherit = ['slide.channel.partner']

    @api.model
    def create(self, values):

        res = super(inheritslidechannelpartner, self).create(values)

        if res.channel_id:
            if res.channel_id.online_class:
                for rec in res.channel_id.event_event_ids:
                    new_attendy = self.env['event.registration'].create({'partner_id':res.partner_id.id,'event_id': rec.id})
        return res               
    