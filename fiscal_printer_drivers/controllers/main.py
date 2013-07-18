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
from fiscal import FiscalPrinterEx
from stoqdrivers.printers import base
from stoqdrivers.enum import PaymentMethodType, TaxType, UnitType
from serial import SerialException
from decimal import Decimal

class FiscalPrinterController(openerp.addons.web.http.Controller):

    _cp_path = '/fiscal_printer'

    def _get_driver(self,printer):        
        fiscal = FiscalPrinterEx(brand=printer.get('brand'),
                    model=printer.get('model'),
                    device=printer.get('port'))
        return fiscal
    
    def _check_printer_serial(self,printer,driver):
        serial = driver.get_serial()
        if serial <> printer.get('serial'):
            raise Exception("The connected printer does not match with the configured for this POS")
        return True
    
    def _check_printer_status(self,printer):
        driver = self._get_driver(printer)
        driver.check_printer_status()
        self._check_printer_serial(printer,driver)
        
    def read_workstation(self,request):
        return{"workstation":gethostname()}
        
    def read_printer_serial(self,request):
        printer = eval(request.get('printer'))
        serial =""
        driver = self._get_driver(printer)
        serial = driver.get_serial()
        return {"serial":serial}
        
    def read_payment_methods(self,request):
        printer = eval(request.get('printer'))
        params = eval(request.get('params'))
        payment_methods = params.get('payment_methods')
        driver = self._get_driver(printer)
        payment_methods = driver.get_payment_constants()
        return ""
        
    def write_payment_methods(self,request):
        printer = eval(request.get('printer'))
        params = eval(request.get('params'))
        payment_methods =params.get('payment_methods')
        driver = self._get_driver(printer)
        driver.set_payment_methods(payment_methods)
        return {"exec":True} 
        
    def read_tax_rates(self,request):
        printer = eval(request.get('printer'))
        payment_methods =[]
        driver = self._get_driver(printer)
        tax_rates = driver.get_tax_constants()
        return {"tax_rates":tax_rates}
        
    def write_tax_rates(self,request):
        printer = eval(request.get('printer'))
        params = eval(request.get('params'))
        tax_rates = params.get('tax_rates')
        driver = self._get_driver(printer)
        pdb.set_trace()
        driver.set_tax_rates(tax_rates)
    
    def read_headers(self,request):
        printer = eval(request.get('printer'))
        headers =[]
        driver = self._get_driver(printer)
        headers = driver.get_coupon_headers()
        return {"headers":headers}
        
    def write_headers(self,request):
        printer = eval(request.get('printer'))
        params = eval(request.get('params'))
        headers = params.get('headers')
        driver = self._get_driver(printer)
        driver.set_coupon_headers(headers)
        return {"exec":True}
        
    def read_footers(self,request):
        printer = eval(request.get('printer'))
        footers =[]
        driver = self._get_driver(printer)
        footers = driver.get_coupon_footers()
        return {"footers":footers}
        
    def write_footers(self,request):
        printer = eval(request.get('printer'))
        params = eval(request.get('params'))
        footers = params.get('footers')
        driver = self._get_driver(printer)
        driver.set_coupon_footers(footers)
        return {"exec":True}
        
    def get_supported_printers(self, request): 
        printers = base.get_supported_printers()
        for brand in printers:
            for i in range(0,len(printers[brand])):
                printers[brand][i] = str(printers[brand][i]).split(".")[3]
        return printers
    
    
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
    
    def _print_receipt(self,receipt):
        printer = receipt.get('printer')
        client = receipt.get('client')
        order_lines = receipt.get('orderlines')
        payment_lines = receipt.get('paymentlines') 
        printer_status = self._check_printer_status(printer)
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
       
            
    @openerp.addons.web.http.jsonrequest
    def print_receipt(self, request, receipt):
        try:
            self._check_printer_params(receipt)
            return self._print_receipt(receipt) 
        except Exception as e:
            return {"status":"error","error":str(e)}
    
    @openerp.addons.web.http.jsonrequest
    def check_printer_status(self, request,printer):
        try:
            self._check_printer_status(printer)
            return {"status":"ok"}
        except Exception as e:
            return {"status":"error","error":str(e)}
        
    @openerp.addons.web.http.httprequest
    def index(self, req, s_action=None, db=None, **kw):
        try:
            values = getattr(self,kw['command'])(kw)
            response = {"status": 'ok',"values": values}
            return json.dumps(response)
        except Exception as e:
            response = {"status":'error',"error": str(e)}
            return json.dumps(response)
        
