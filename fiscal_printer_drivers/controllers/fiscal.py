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

from stoqdrivers.printers.fiscal import FiscalPrinter
from stoqdrivers.printers import base
from stoqdrivers.exceptions import DriverError
from stoqdrivers.translation import stoqdrivers_gettext
_ = stoqdrivers_gettext
from kiwi.log import Logger
log = Logger('fiscalex')

class FiscalPrinterEx(FiscalPrinter):
    
    def get_supported_printers(self):
        printers = base.get_supported_printers()
        for brand in printers:
            for i in range(0,len(printers[brand])):
                printers[brand][i] = str(printers[brand][i]).split(".")[3]
        return printers
    
    def get_supported_printers(self):
        return base.get_supported_printers()
        
    def set_payment_methods(self,payment_methods):
        log.info('set_payment_methods()')        
        if hasattr(self._driver,'set_payment_methods'):              
            self._driver.set_payment_methods(payment_methods)
        else:
            raise DriverError(_("This method is not supported from "
                                "the current printer"))    

    def set_tax_rates(self,tax_rates):
        log.info('set_tax_rates()')        
        if hasattr(self._driver,'set_tax_rates'):              
            self._driver.set_tax_rates(tax_rates)
        else:
            raise DriverError(_("This method is not supported from "
                                "the current printer"))
        
    def set_tax_rates(self,tax_rates):
        log.info('set_tax_rates()')        
        if hasattr(self._driver,'set_tax_rates'):              
            self._driver.set_tax_rates(tax_rates)
        else:
            raise DriverError(_("This method is not supported from "
                                "the current printer"))        
    def get_coupon_headers(self):
        log.info('get_coupon_headers()')   
        headers = []     
        if hasattr(self._driver,'get_coupon_headers'):              
            headers = self._driver.get_coupon_headers()
        else:
            raise DriverError(_("This method is not supported from "
                                "the current printer"))
        return headers
                                
    def set_coupon_headers(self,headers):
        log.info('set_coupon_headers()')        
        if hasattr(self._driver,'set_coupon_headers'):              
            self._driver.set_coupon_headers(headers)
        else:
            raise DriverError(_("This method is not supported from "
                                "the current printer"))
    
    def get_coupon_footers(self):
        log.info('get_coupon_footers()')   
        footers = []     
        if hasattr(self._driver,'get_coupon_footers'):              
            footers = self._driver.get_coupon_footers()
        else:
            raise DriverError(_("This method is not supported from "
                                "the current printer"))
        return footers
    
    
    def set_coupon_footers(self,footers):
        log.info('set_coupon_footers()')        
        if hasattr(self._driver,'set_coupon_footers'):              
            self._driver.set_coupon_footers(footers)
        else:
            raise DriverError(_("This method is not supported from "
                                "the current printer"))
    def check_printer_status(self):
        self._driver._check_error()
