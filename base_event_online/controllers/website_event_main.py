# -*- coding: utf-8 -*-
import logging
import re

import werkzeug
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.web.controllers.main import ensure_db

import odoo
from odoo import http, _
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteEventControllerInherit(WebsiteEventController):
    @http.route(['''/event/<model("event.event", "[('website_id', 'in', (False, current_website_id))]"):event>/register'''], type='http', auth="public", website=True, sitemap=False)
    def event_register(self, event, **post):
        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        urls = event._get_event_resource_urls()
        current_partner = request.env['res.users'].search([('id','=',request.session.uid)]).partner_id
        user_registration = request.env['event.registration'].sudo().search([('event_id','=',event.id),('partner_id','=',current_partner.id)],order='id desc',limit=1)
        
        values = {
            'event': event,
            'user_registration_object': user_registration,
            'main_object': event,
            'range': range,
            'registrable': event.sudo()._is_event_registrable(),
            'google_url': urls.get('google_url'),
            'iCal_url': urls.get('iCal_url'),
        }
        return request.render("website_event.event_description_full", values)