
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################




from odoo import models, fields, api
import time
from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
from datetime import datetime
from dateutil.relativedelta import relativedelta



class inheritSlideChannel(models.Model):
    _inherit = ["slide.channel"]

    web_session_type = fields.Selection(selection_add=[('odoo_zoom_eLearning', 'Zoom'),])



   
    def write(self, values):
        obj_write = super(inheritSlideChannel, self).write(values)

        for rec in self.event_event_ids:
            rec.slide_channel_id = self.id
    
        return obj_write

    
    
   