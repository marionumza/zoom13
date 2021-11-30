
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

class inheritSlideChannel(models.Model):
    _inherit = ["slide.channel"]

    online_class = fields.Boolean(string='',
    default=False
    )

    
    web_session_type = fields.Selection([], string='Web Session',)
    
    event_event_ids = fields.Many2many(
        string="Event Event", comodel_name="event.event",
        compute="comp_event_event_ids"
    )


    def comp_event_event_ids(self):
        for rec in self:
            course_event_lines = self.env["event.event"].sudo().search([("slide_channel_id", "=", rec.id)])
            rec.event_event_ids =  [(6, 0, course_event_lines.ids)]


    lec_count = fields.Char(compute="_compute_lec_count", string="")

    @api.depends("event_event_ids")
    def _compute_lec_count(self):
        for rec in self:
            rec.lec_count = self.env["event.event"].search_count(
                [("slide_channel_id", "=", rec.id)]
            )

    def return_lectires(self):

        view_ref = self.env["ir.model.data"].get_object_reference(
            "odoo_zoom", "online_event_event_tree"
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "event.event",
            "name": "Lectures",
            "view_ids": "[(6, 0, 0),(0, 0, {'view_mode': 'tree', 'view_id': ref('odoo_zoom.online_event_event_tree')})]",
            "view_mode": "tree",
            "domain": [("id", "in", self.event_event_ids.ids)],
        }
