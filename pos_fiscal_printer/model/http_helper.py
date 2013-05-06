from openerp.osv import osv, fields
from openerp.osv.orm import except_orm
from urllib2 import URLError,HTTPError
import urllib
import urllib2
import json


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
    
    def _get_request(self, cr, uid,name,params):
        
        obj = self.browse(cr, uid, self.search(cr, uid, []))[0]    
        url = obj.proxy_url+name
        if (params):
            url += "?" + urllib.urlencode(params,True)
        request = urllib2.Request(url)
        return request
    
    def send_request(self, cr, uid,name,*args,**kwargs):
       
        request = self._get_request(cr, uid,name,kwargs)
        try:
            response = urllib2.urlopen(request) 
        except HTTPError:
            self._print_error("HTTP Error !",
                "Command not found")
        except URLError:
            self._print_error("Could not connect !",
                "Connection to local proxy is refused")
        return json.loads(response.read())
