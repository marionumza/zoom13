
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


class inheritEventeLearningZoom(models.Model):

    _inherit = ["event.event"]


    def odoo_zoom_eLearning_close(self):
        for rec in self:
            temp_key = rec.temp_key

            headers = {
                    'content-type': "application/json",
                    'authorization': "Bearer " + temp_key
                    }
                    

            server_url = self.env['ir.config_parameter'].sudo().get_param('base_event_online.zm_server_url')           

            if not (server_url):
                raise ValidationError(_("Please Configure Zoom Server Global Configuration"))

            url = server_url + "/meetings/"+ rec.meeting_id + "/status"
            payload = "{\"action\":\"end\"}"            
            response = requests.request("PUT", url, data=payload,headers= headers)
            print ('#>>Zoom ending response of Api>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' )

            print (response.status_code )

            if response.status_code == 204:
                print ('#>>Zoom MEETING closed SUCCESS>>>>>>>>>>MOD:>odoo_zoom_eLearning>>>>>>>>>' )

                return True



    def button_done(self):
        if self.is_elearning_event:
            if self.slide_channel_id.web_session_type =='odoo_zoom_eLearning':  
                if self.odoo_zoom_eLearning_close():
                    
                    self.is_meeting_active = False
                    for registration_ids in self.registration_ids:
                        registration_ids.is_active = False                  

        res = super(inheritEventeLearningZoom, self).button_done()
    



    def zoom_call_initiate(self,url,key,payload,show_message):
  
        print("zoom-call-initiate")
        
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + key
            }

        try:
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            json_response = json.loads(response.text)

        except Exception as e:
            _logger.info('----Exception-------')
            _logger.info(e)  
            return False

        if response.status_code == 201:
            _logger.info('---valid response code-------')

            self.sudo().write({
                'public_url':json_response['join_url'],
                'meeting_id':json_response['id'],
                'moderator_url':json_response['start_url'],
                'temp_key':key,
                'is_published':True,
                'is_meeting_active':True,
            })

            for registration_ids in self.registration_ids:
                registration_ids.is_active = True                
            return True
        else:
            if show_message:
                _logger.info('---invalid response code-------')
                _logger.info(response.status_code)  
                raise ValidationError(_(ast.literal_eval(response.text)['message']))

            



    def initiate_from_user_conf(self,server_url,payload):
        for rec in self:

            user_e_mail = self.user_id.zoom_email
            key = self.user_id.zoom_secret_key


            if not (user_e_mail or key):
                return False

            url = server_url+ "/users/" + user_e_mail + "/meetings"
            show_message = False

            return self.zoom_call_initiate(url,key,payload,show_message)       

         

    def initiate_zoom_classeLearning(self):
        for rec in self:
            server_url = self.env['ir.config_parameter'].sudo().get_param('base_event_online.zm_server_url')
            if not (server_url):
                raise ValidationError(_("Please Configure Global Zoom Configuration"))          
        
            if not rec.moderator_password:
                raise ValidationError(_("Please Provide Moderator Password to initiate meeting"))           
            
            payload = {
                    "topic":rec.name,
                    "type":"1",
                    "password":rec.moderator_password,
                    "agenda":rec.name,
                    "recurrence":{"type":"2"},
                    "settings":{"approval_type":"2"}                    
                    }
    
            call_end = self.initiate_from_user_conf(server_url,payload)

            if call_end:
                return True
                
            global_e_mail =self.env['ir.config_parameter'].sudo().get_param('base_event_online.e_mail')
            global_zoom_key =self.env['ir.config_parameter'].sudo().get_param('base_event_online.zoom_secret_key')       

            if not (global_e_mail):
                raise ValidationError(_("Please Configure Global Zoom Authentication E Mail"))

            if not (global_zoom_key):
                raise ValidationError(_("Please Configure Global Zoom Authentication Key"))
        

            url = server_url+ "/users/" + global_e_mail + "/meetings"
            show_message = True

            if not self.zoom_call_initiate(url,global_zoom_key,payload,show_message):
                raise ValidationError(_("Zoom Meeting is not Initiated due to error in configuration"))
 
    

    def initiate_elearning_class_event(self):

            res = super(inheritEventeLearningZoom, self).initiate_elearning_class_event()
            print (">>>method>>>>>inheritEventeLearningZoom>>>>>>>>>>>>>>>>CLASS>>>>inheritEventeLearningZoom")

            if not self.slide_channel_id.web_session_type:
                raise ValidationError(_("Please Configure Meeting Type Properly"))           



            if self.slide_channel_id.web_session_type =='odoo_zoom_eLearning':
                self.initiate_zoom_classeLearning()






