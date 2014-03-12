# -*- coding: utf-8 -*-
import logging
import simplejson
import os
import os.path
import openerp
import time
import random
import subprocess
import simplejson
import werkzeug
import werkzeug.wrappers
_logger = logging.getLogger(__name__)

from openerp.addons.web.controllers.main import manifest_list, module_boot, html_template


# drivers modules must add to drivers an object with a get_status() method 
# so that 'status' can return the status of all active drivers
drivers = {}

class Proxy(openerp.addons.web.http.Controller):
    
    _cp_path='/hw_proxy'

    def __init__(self):
        self.scale = 'closed'
        self.scale_weight = 0.0

    def get_status(self):
        statuses = {}
        for driver in drivers:
            statuses[driver] = drivers[driver].get_status()
        return statuses

    @openerp.addons.web.http.httprequest
    def hello(self, request):
        return "ping"

    @openerp.addons.web.http.jsonrequest
    def handshake(self, request):
        return True

    @openerp.addons.web.http.httprequest
    def status_http(self, request):
        resp = '<html>\n<body>\n<h1>Hardware Proxy Status</h1>\n'
        statuses = self.get_status()
        for driver in statuses:

            status = statuses[driver]

            if status['status'] == 'connecting':
                color = 'black'
            elif status['status'] == 'connected':
                color = 'green'
            else:
                color = 'red'

            resp += "<h2 style='color:"+color+";'>"+driver+' : '+status['status']+"</h2>\n"
            resp += "<ul>\n"
            for msg in status['messages']:
                resp += '<li>'+msg+'</li>\n'
            resp += "</ul>\n"
        resp += "<script>\n\tsetTimeout(function(){window.location.reload();},30000);\n</script>\n</body>\n</html>\n\n"

        return request.make_response(resp,{
            'Cache-Control': 'no-cache', 
            'Content-Type': 'text/html; charset=utf-8',
            'Access-Control-Allow-Origin':  '*',
            'Access-Control-Allow-Methods': 'GET',
            })

    @openerp.addons.web.http.jsonrequest
    def status_json(self, request):
        return self.get_status()

    @openerp.addons.web.http.jsonrequest
    def scan_item_success(self, request, ean):
        """
        A product has been scanned with success
        """
        print 'scan_item_success: ' + str(ean)

    @openerp.addons.web.http.jsonrequest
    def scan_item_error_unrecognized(self, request, ean):
        """
        A product has been scanned without success
        """
        print 'scan_item_error_unrecognized: ' + str(ean)

    @openerp.addons.web.http.jsonrequest
    def help_needed(self, request):
        """
        The user wants an help (ex: light is on)
        """
        print "help_needed"

    @openerp.addons.web.http.jsonrequest
    def help_canceled(self, request):
        """
        The user stops the help request
        """
        print "help_canceled"

    @openerp.addons.web.http.jsonrequest
    def weighting_start(self, request):
        if self.scale == 'closed':
            print "Opening (Fake) Connection to Scale..."
            self.scale = 'open'
            self.scale_weight = 0.0
            time.sleep(0.1)
            print "... Scale Open."
        else:
            print "WARNING: Scale already Connected !!!"

    @openerp.addons.web.http.jsonrequest
    def weighting_read_kg(self, request):
        if self.scale == 'open':
            print "Reading Scale..."
            time.sleep(0.025)
            self.scale_weight += 0.01
            print "... Done."
            return self.scale_weight
        else:
            print "WARNING: Reading closed scale !!!"
            return 0.0

    @openerp.addons.web.http.jsonrequest
    def weighting_end(self, request):
        if self.scale == 'open':
            print "Closing Connection to Scale ..."
            self.scale = 'closed'
            self.scale_weight = 0.0
            time.sleep(0.1)
            print "... Scale Closed."
        else:
            print "WARNING: Scale already Closed !!!"

    @openerp.addons.web.http.jsonrequest
    def payment_request(self, request, price):
        """
        The PoS will activate the method payment 
        """
        print "payment_request: price:"+str(price)
        return 'ok'

    @openerp.addons.web.http.jsonrequest
    def payment_status(self, request):
        print "payment_status"
        return { 'status':'waiting' } 

    @openerp.addons.web.http.jsonrequest
    def payment_cancel(self, request):
        print "payment_cancel"

    @openerp.addons.web.http.jsonrequest
    def transaction_start(self, request):
        print 'transaction_start'

    @openerp.addons.web.http.jsonrequest
    def transaction_end(self, request):
        print 'transaction_end'

    @openerp.addons.web.http.jsonrequest
    def cashier_mode_activated(self, request):
        print 'cashier_mode_activated'

    @openerp.addons.web.http.jsonrequest
    def cashier_mode_deactivated(self, request):
        print 'cashier_mode_deactivated'

    @openerp.addons.web.http.jsonrequest
    def open_cashbox(self, request):
        print 'open_cashbox'

    @openerp.addons.web.http.jsonrequest
    def print_receipt(self, request, receipt):
        print 'print_receipt' + str(receipt)

    @openerp.addons.web.http.jsonrequest
    def is_scanner_connected(self, request, receipt):
        print 'is_scanner_connected?' 
        return False

    @openerp.addons.web.http.jsonrequest
    def scanner(self, request, receipt):
        print 'scanner' 
        time.sleep(10)
        return ''

    @openerp.addons.web.http.jsonrequest
    def log(self, arguments):
        _logger.info(' '.join(str(v) for v in arguments))

    @openerp.addons.web.http.jsonrequest
    def print_pdf_invoice(self, request, pdfinvoice):
        print 'print_pdf_invoice' + str(pdfinvoice)


