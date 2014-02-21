from openerp.osv.orm import except_orm
from openerp.osv import osv, fields
from openerp.tools.translate import _
import urllib
import urllib2
from urllib2 import URLError, HTTPError
import json


class generic_device(osv.Model):

    _name = "generic.device"

    def _print_error(self, error, msg):
        '''
        shows an error on the screen
        '''
        raise osv.except_osv(error, msg)
                          
    def _get_device(self, cr, uid, ids,context=None):
        if not ids:
            return []
        fields = self.read(cr,uid,ids,context=context)[0]
        for field in fields:
            value =  fields[field]
            if isinstance(value,tuple):
                fields[field] = self.resolve_2many_commands(cr,uid,field,[value[0]])[0]
            elif isinstance(value,list):
                fields[field] = self.resolve_2many_commands(cr,uid,field,value)
        return fields
       

    def _make_command(self, cr, uid, ids, command, params, context=None):
        context = context or {}
        remote_address = context.get('remote_addr') or '127.0.0.1'
        url = "http://"+remote_address+":8069/hw_proxy/"+command  
        req_params = {'params':params}
        req_params_str = urllib.urlencode(req_params)
        request = urllib2.Request(url, req_params_str)
        return request

    def send_command(self, cr, uid, ids, command, params={}, context=None):

        context = context or {}
        response = {}
        request = self._make_command(cr, uid, ids, command, params, context=context)
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
            self._print_error("COMMAND ERROR", response['error'])
        return response['values']
