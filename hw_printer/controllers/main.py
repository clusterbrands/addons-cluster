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

import logging
import simplejson
import os
import openerp
import pdb
import json
from socket import gethostname
from serial import SerialException
from decimal import Decimal
from threading import Thread, Lock
from Queue import Queue, Empty
from openerp import http
from openerp.http import request
import openerp.addons.hw_proxy.controllers.main as hw_proxy
from .. import driver
from ..driver import fiscal
from ..driver.fiscal import FiscalPrinterEx

try:
    from stoqdrivers.printers import base
    from stoqdrivers.enum import PaymentMethodType, TaxType, UnitType
except ImportError:
    base = None
    PaymentMethodType = None
    TaxType = None
    UnitType = None

_logger = logging.getLogger(__name__)

class FiscalPrinterDriver(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.lock  = Lock()      

    def _get_driver(self,printer):      
        fiscal = FiscalPrinterEx(brand=printer.get('brand').get("name"),
                    model=printer.get('model').get("name"),
                    device=printer.get('port'))
        return fiscal
    
    def check_printer_serial(self, printer):
        driver = self._get_driver(printer)
        serial = driver.get_serial()
        if serial <> printer.get('serial'):
            raise Exception("The connected printer does not match with the configured for this POS")
        return True
    
    def check_printer_status(self, params):
        reponse = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:            
            driver = self._get_driver(printer)
            driver.check_printer_status()
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()  
        return response

    def _check_printer_status(self,printer,params):
        driver = self._get_driver(printer)
        driver.check_printer_status()
        
    def read_workstation(self):
        return{"workstation":gethostname()}
        
    def read_printer_serial(self, params):
        reponse = {}
        self.lock.acquire()
        try:            
            driver = self._get_driver(params.get('printer'))
            serial = driver.get_serial()
            response = {"serial":serial}          
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()  
        return response
        
    def read_payment_methods(self, params):
        response = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            driver = self._get_driver(printer)
            response = {"payment_methods: ":driver.get_payment_constants()}
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response
        
    def write_payment_methods(self, params):
        response = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:            
            self.check_printer_serial(printer)
            payment_methods = params.get('payment_methods')
            driver = self._get_driver(printer)
            driver.set_payment_methods(payment_methods)
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response
        
    def read_tax_rates(self, params):
        response = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            driver = self._get_driver(printer)
            tax_rates = driver.get_tax_constants()
            response = {"tax_rates":tax_rates}
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response
        
    def write_tax_rates(self, params):
        response = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            tax_rates = params.get('tax_rates')
            driver = self._get_driver(printer)
            driver.set_tax_rates(tax_rates)
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response
    
    def read_headers(self, params):
        response = {}
        headers =[]
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            driver = self._get_driver(printer)
            headers = driver.get_coupon_headers()
            response = {"headers":headers}
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response
        
    def write_headers(self, params):
        response = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            headers = params.get('headers')
            driver = self._get_driver(printer)
            driver.set_coupon_headers(headers)
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response    
        
    def read_footers(self, params):
        response = {}
        footers =[]
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            driver = self._get_driver(printer)
            footers = driver.get_coupon_footers()
            response = {"footers":footers}
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response
        
    def write_footers(self, params):
        response = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            footers = params.get('footers')
            driver = self._get_driver(printer)
            driver.set_coupon_footers(footers)
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response
        
    def get_supported_printers(self): 
        printers = base.get_supported_printers()
        for brand in printers:
            for i in range(0,len(printers[brand])):
                printers[brand][i] = str(printers[brand][i]).split(".")[3]
        return printers
        
    def has_pending_reduce(self, params):
        response = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            driver = self._get_driver(printer)
            response = {"reduce":driver.has_pending_reduce()}
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response

    def print_report_x(self, printer):
        response = {}
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            driver = self._get_driver(printer)
            report_number = driver.summarize()
            response  = {"report_number":report_number,"printer_serial":printer.get("serial")}  
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response

    def print_report_z(self, params):
        response = {}
        printer = params.get('printer')
        self.lock.acquire()
        try:
            self.check_printer_serial(printer)
            driver = self._get_driver(printer)
            report_number = driver.close_till()
            return {"report_number":report_number,"printer_serial":printer.get("serial")}
        except Exception as e :
            response = {"status":"error", "reason":str(e)}
        self.lock.release()
        return response     
    
    def _add_items(self,driver,order_lines):
        for product in order_lines:
            driver.add_item(
                "",
                str(product.get('product_name')),
                Decimal(product.get('price_with_tax')),
                str(product.get('tax_code')),
                items_quantity= Decimal(product.get('quantity')),
                unit = UnitType.CUSTOM, 
                discount = Decimal(product.get('discount')),
                unit_desc = ("%-2s") % str(product.get('unit_code'))
            )
    
    def _open_coupon(self,driver):
        if (driver.has_open_coupon()):
            driver.cancel()
        driver.open()            
            
    def _add_payments(self,driver,payment_lines):
        for payment in payment_lines:
            driver.add_payment(
                str(payment.get('payment_method_code')),
                Decimal(payment.get('amount'))
            )            
    
    def _check_printer_params(self,receipt):
        order_lines = receipt.get('orderlines')
        payment_lines = receipt.get('paymentlines')
        for product in order_lines:
            if (product.get('tax_code') == ""):
                raise Exception("The product : '"+
                    product.get('product_name') +
                    "' does not have a tax rate configured for the current printer")
            if (product.get('unit_code') == ""):
                  raise Exception("The product : '"+
                    product.get('product_name') +
                    "' does not have a measure unit configured for the current printer")
        for payment in payment_lines:
            if (payment.get('payment_method_code') == ""):
                raise Exception("The payment method "+
                    payment.get("journal")+" is not configured for the current printer")        
    
    def _print_receipt(self,receipt,printer):
        client = receipt.get('client')
        order_lines = receipt.get('orderlines')
        payment_lines = receipt.get('paymentlines') 
        printer_status = self.check_printer_status(printer,{})
        self.check_printer_serial(printer)
        driver = self._get_driver(printer)
        driver.identify_customer(str(client.get('name')),
           str(client.get('address')), str(client.get('vat')))
        self._open_coupon(driver)           
        try:
            self._add_items(driver,order_lines)
            driver.totalize()
            self._add_payments(driver,payment_lines)  
            receipt_id = driver.close()
            return {"status":"ok","receipt_id":receipt_id,"serial":printer.get('serial')}
        except Exception as e:
            driver.cancel()
            return {"status":"error","error":str(e)}            
       
    def print_receipt(self, receipt, printer):
        try:
            self._check_printer_params(receipt)
        except Exception as e:
            return {"status":"error","error":str(e)}
        return self._print_receipt(receipt,printer)   

driver = FiscalPrinterDriver()
hw_proxy.drivers['fiscalprinter'] = driver

class FiscalPrinterProxy(hw_proxy.Proxy):
   
    @http.route('/hw_proxy/get_supported_printers', type='http', auth='none', cors='*')
    def get_supported_printers(self, params):
        return json.dumps(driver.get_supported_printers())

    @http.route('/hw_proxy/read_workstation', type='http', auth='none', cors='*')
    def read_workstation(self, params):
        return json.dumps(driver.read_workstation())

    @http.route('/hw_proxy/read_printer_serial', type='http', auth='none', cors='*')
    def read_printer_serial(self, params):
        return json.dumps(driver.read_printer_serial(eval(params)))

    @http.route('/hw_proxy/read_payment_methods', type='http', auth='none', cors='*')
    def read_payment_methods(self, params):
        return json.dumps(driver.read_payment_methods(eval(params)))

    @http.route('/hw_proxy/write_payment_methods', type='http', auth='none', cors='*')
    def write_payment_methods(self, params):
        return json.dumps(driver.write_payment_methods(eval(params)))

    @http.route('/hw_proxy/read_tax_rates', type='http', auth='none', cors='*')
    def read_tax_rates(self, params):
        return json.dumps(driver.read_tax_rates(eval(params)))

    @http.route('/hw_proxy/write_tax_rates', type='http', auth='none', cors='*')
    def write_tax_rates(self, params):
        return json.dumps(driver.write_tax_rates(eval(params)))

    @http.route('/hw_proxy/read_headers', type='http', auth='none', cors='*')
    def read_headers(self, params):
        return json.dumps(driver.read_headers(eval(params)))

    @http.route('/hw_proxy/write_headers', type='http', auth='none', cors='*')
    def write_headers(self, params):
        return json.dumps(driver.write_headers(eval(params)))

    @http.route('/hw_proxy/read_footers', type='http', auth='none', cors='*')
    def read_footers(self, params):
        return json.dumps(driver.read_footers(eval(params)))

    @http.route('/hw_proxy/write_footers', type='http', auth='none', cors='*')
    def write_footers(self, params):
        return json.dumps(driver.write_footers(eval(params)))

    @http.route('/hw_proxy/print_report_x', type='json', auth='none', cors='*')
    def print_report_x_json(self, printer):
        return driver.print_report_x(printer)

    @http.route('/hw_proxy/print_report_x', type='http', auth='none', cors='*')
    def print_report_x_http(self, params):
        params = eval(params)
        return json.dumps(driver.print_report_x(params.get('printer')))

    @http.route('/hw_proxy/print_report_z', type='http', auth='none', cors='*')
    def print_report_z(self, params):
        return json.dumps(driver.print_report_z(eval(params)))

    @http.route('/hw_proxy/print_receipt', type='json', auth='none', cors='*')
    def print_receipt(self, receipt, printer):
        return driver.print_receipt(receipt, printer)

    @http.route('/hw_proxy/check_printer_status', type='json', auth='none', cors='*')
    def check_printer_status(self, params):
        return driver.check_printer_status(params)

    @http.route('/hw_proxy/has_pending_reduce', type='http', auth='none', cors='*')
    def has_pending_reduce(self, params):
        return json.dumps(driver.has_pending_reduce(eval(params)))