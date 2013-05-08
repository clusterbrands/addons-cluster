import logging
import simplejson
import os
import openerp
import pdb
import json
from point_of_sale.controllers.main import PointOfSaleController
from stoqdrivers.printers import base
from stoqdrivers.printers.fiscal import FiscalPrinter
from serial import SerialException

class CustomProxy(PointOfSaleController):

    def __init__(self):
        super(CustomProxy,self).__init__()
    
    

    def _get_driver(self,printer):        
        fiscal = FiscalPrinter(brand=printer.get('brand'),
                    model=printer.get('model'),
                    device=printer.get('port'))
        return fiscal    
    
    def read_printer_serial(self,request):
        printer = eval(request.get('printer'))
        serial =""
        try:
            driver = self._get_driver(printer)
        except SerialException as e:
            raise
        serial = driver.get_serial()
        return {"serial":serial}
        
    def read_payment_methods(self,request):
        printer = eval(request.get('printer'))
        payment_methods =[]
        try:
            driver = self._get_driver(printer)
        except SerialException as e:
            raise
        payment_methods = driver.get_payment_constants()
        return {"payment_methods":payment_methods}
        
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
        
