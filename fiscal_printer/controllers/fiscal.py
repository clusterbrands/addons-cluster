from stoqdrivers.printers.fiscal import FiscalPrinter
from stoqdrivers.printers import base
from stoqdrivers.exceptions import DriverError
from kiwi.log import Logger
from stoqdrivers.translation import stoqdrivers_gettext
_ = stoqdrivers_gettext
log = Logger('fiscalex')

class FiscalPrinterEx(FiscalPrinter):
    
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
