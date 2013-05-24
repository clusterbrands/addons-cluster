#!/usr/bin/python
# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Eduardo Ochoa    <eduardo.ochoa@clusterbrands.com.ve>
#                               <elos3000@gmail.com>
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

from openerp.osv import osv, fields
from openerp.osv.orm import except_orm
from urllib2 import URLError,HTTPError
import urllib
import urllib2
import json
import pdb


class http_helper(osv.Model):
    
    _name = 'pos_fiscal_printer.http_helper'
    _columns = {
        'connection_name': fields.char('Connection Name',size=255,
            required=True),
        'proxy_url': fields.char('Local Proxy Url',size=255,
            required=True)
    }
    
    def _print_error(self, error, msg):
        '''
        shows an error on the screen
        '''
        raise osv.except_osv(error, msg)
        
    def _get_printer(self,cr,uid,ids):
        if ids:
            p_obj = self.pool.get('pos_fiscal_printer.printer')
            printer = p_obj.browse(cr,uid,ids)[0]            
            return {
                    'brand':printer.brand.brand_name,
                    'model':printer.model.model_name,
                    'port':printer.port
                    }
        else:
            return {}
    
    def _make_command(self, cr, uid,ids,name,params):    
        
        obj = self.browse(cr, uid, self.search(cr, uid, []))[0]    
        url = obj.proxy_url 
        params = params or {}       
        printer = self._get_printer(cr,uid,ids)
        req_params = {'command':name,'printer':printer,'params':params}
        req_params_str = urllib.urlencode(req_params)
        request = urllib2.Request(url,req_params_str)
        return request
    
    def send_command(self, cr, uid,ids,name,params={}):       
        
        request = self._make_command(cr, uid,ids,name,params)
        try:
            response = urllib2.urlopen(request) 
        except HTTPError as e:
            self._print_error("HTTP ERROR !",
                e.reason.decode('utf-8'))
        except URLError as e:
            self._print_error("URL ERROR !",
                e.reason.strerror.decode('utf-8'))

        response = json.loads(response.read())
        if response['status'] == 'error':
            self._print_error("COMMAND ERROR",response['error'])
        return response['values']
