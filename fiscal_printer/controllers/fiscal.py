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
        
    def set_tax_rates(self,tax_rates):
        log.info('set_tax_rates()')        
        if hasattr(self._driver,'set_tax_rates'):              
            self._driver.set_tax_rates(tax_rates)
        else:
            raise DriverError(_("This method is not supported from "
                                "the current printer"))
        
    
        
