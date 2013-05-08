import logging
import simplejson
import os
import openerp
import pdb
import json
from point_of_sale.controllers.main import PointOfSaleController
from stoqdrivers.printers import base
from stoqdrivers.printers.fiscal import FiscalPrinter
class CustomProxy(PointOfSaleController):

    def __init__(self):
        super(CustomProxy,self).__init__()
    
    

    def _get_printer_driver(self,printer):        
        fiscal = FiscalPrinter(brand=printer['brand'],model=printer['model'],
                    device=printer['port'])
        return fiscal    
    
    def read_printer_serial(self,request):
        printer = eval(request['printer'])
        self._get_printer_driver(printer)
    
    def get_supported_printers(self, request): 
        printers = base.get_supported_printers()
        for brand in printers:
            for i in range(0,len(printers[brand])):
                printers[brand][i] = str(printers[brand][i]).split(".")[3]
        return printers
    
    
    @openerp.addons.web.http.jsonrequest
    def print_receipt(self, request, receipt):
        return ""   
        
    @openerp.addons.web.http.httprequest
    def index(self, req, s_action=None, db=None, **kw):
        try:
            values = getattr(self,kw['command'])(kw)
            response = {"status": 'ok',"values": values}
            return json.dumps(response)
        except Exception as e:
            response = {"status":'error',"error": str(e)}
            return json.dumps(response)
        
