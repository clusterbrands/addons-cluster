import logging
import simplejson
import os
import openerp
import pdb
import json
from point_of_sale.controllers.main import PointOfSaleController
from stoqdrivers.printers import base,fiscal
class CustomProxy(PointOfSaleController):

    def __init__(self):
        super(CustomProxy,self).__init__()
    
    @openerp.addons.web.http.jsonrequest
    def print_receipt(self, request, receipt):
        import pdb
        pdb.set_trace()
        return 'two doorss'
    
    @openerp.addons.web.http.httprequest
    def get_supported_brands(self, req, s_action=None, db=None, **kw):
        printers = base.get_supported_printers()
        brands = printers.keys()
        return json.dumps(brands)
        
    @openerp.addons.web.http.httprequest
    def get_supported_printers(self, req, s_action=None, db=None, **kw): 
        print "REQ, %s " % req.httprequest.args.keys()       
        printers = base.get_supported_printers()
        for brand in printers:
            for i in range(0,len(printers[brand])):
                printers[brand][i] = str(printers[brand][i]).split(".")[3]
        return json.dumps(printers)
        
