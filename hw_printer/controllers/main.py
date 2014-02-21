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
import openerp.addons.hw_proxy.controllers.main as hw_proxy

try:
    from .. import driver
    from ..driver import fiscal
    from fiscal import FiscalPrinterEx
    from stoqdrivers.printers import base
    from stoqdrivers.enum import PaymentMethodType, TaxType, UnitType
except ImportError:
    fiscal = None
    FiscalPrinterEx = None
    base = None
    PaymentMethodType = None
    TaxType = None
    UnitType = None

_logger = logging.getLogger(__name__)

class FiscalPrinterDriver(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.lock  = Lock()
        self.status = {'status':'connecting', 'messages':[]}

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
    
    def check_printer_status(self,printer,params):
        driver = self._get_driver(printer)
        driver.check_printer_status()
        
    def read_workstation(self,printer,params):
        return{"workstation":gethostname()}
        
    def read_printer_serial(self,printer,params):
        serial =""
        driver = self._get_driver(printer)
        serial = driver.get_serial()
        return {"serial":serial}
        
    def read_payment_methods(self, printer, params):
        self.check_printer_serial(printer)
        payment_methods = params.get('payment_methods')
        driver = self._get_driver(printer)
        payment_methods = driver.get_payment_constants()
        return ""
        
    def write_payment_methods(self,printer,params):
        self.check_printer_serial(printer)
        payment_methods =params.get('payment_methods')
        driver = self._get_driver(printer)
        driver.set_payment_methods(payment_methods)
        return {"exec":True} 
        
    def read_tax_rates(self,printer,params):
        self.check_printer_serial(printer)
        payment_methods =[]
        driver = self._get_driver(printer)
        tax_rates = driver.get_tax_constants()
        return {"tax_rates":tax_rates}
        
    def write_tax_rates(self,printer,params):
        self.check_printer_serial(printer)
        tax_rates = params.get('tax_rates')
        driver = self._get_driver(printer)
        driver.set_tax_rates(tax_rates)
    
    def read_headers(self,printer,params):
        self.check_printer_serial(printer)
        headers =[]
        driver = self._get_driver(printer)
        headers = driver.get_coupon_headers()
        return {"headers":headers}
        
    def write_headers(self,printer,params):
        self.check_printer_serial(printer)
        headers = params.get('headers')
        driver = self._get_driver(printer)
        driver.set_coupon_headers(headers)
        return {"exec":True}
        
    def read_footers(self,printer,params):
        self.check_printer_serial(printer)
        footers =[]
        driver = self._get_driver(printer)
        footers = driver.get_coupon_footers()
        return {"footers":footers}
        
    def write_footers(self,printer,params):
        self.check_printer_serial(printer)
        footers = params.get('footers')
        driver = self._get_driver(printer)
        driver.set_coupon_footers(footers)
        return {"exec":True}
        
    def get_supported_printers(self, printer,params): 
        printers = base.get_supported_printers()
        for brand in printers:
            for i in range(0,len(printers[brand])):
                printers[brand][i] = str(printers[brand][i]).split(".")[3]
        return printers
        
    def has_pending_reduce(self, printer, params):
        self.check_printer_serial(printer)
        driver = self._get_driver(printer)
        res = driver.has_pending_reduce()
        return {"reduce":res}

    def print_report_x(self, printer, params):
        self.check_printer_serial(printer)
        driver = self._get_driver(printer)
        report_number = driver.summarize()
        return {"report_number":report_number,"printer_serial":printer.get("serial")}  

    def print_report_z(self, printer, params):
        self.check_printer_serial(printer)
        driver = self._get_driver(printer)
        report_number = driver.close_till()
        return {"report_number":report_number,"printer_serial":printer.get("serial")}     
    
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
       
    def print_receipt(self,printer,params):
        receipt = params.get("receipt")
        self._check_printer_params(receipt)
        return self._print_receipt(receipt,printer) 

driver = FiscalPrinterDriver()
hw_proxy.drivers['fiscalprinter'] = driver

class FiscalPrinterProxy(hw_proxy.Proxy):
    
    @openerp.addons.web.http.httprequest
    def get_supported_printers(self, request, params):
        return json.dumps({})

