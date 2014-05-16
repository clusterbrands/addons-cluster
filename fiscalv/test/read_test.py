"""
This script tests some printer functinoalities, 
only those wich envolve getting data from the printer
"""

import sys, os
sys.path.append(os.path.abspath('..'))

from datetime import datetime
from stoqdrivers.enum import PaymentMethodType, TaxType, UnitType
from stoqdrivers.exceptions import (PendingReduceZ,
                                    PendingReadX,
                                    CouponOpenError,
                                    CloseCouponError,)
from decimal import Decimal

from fiscalv import FiscalV

# Declare printer instance with proper configuration
print "Creating instance"
printer = FiscalV(brand='bematech', model='MP4000', device='/dev/ttyUSB0')

# Get printer status and catch any exception just to be sure it works
print "Trying to get printer status"
try:
    p = printer.get_status_printer()
except CouponOpenError:
    print "Printer has a coupon currently open, lets cancel"
    printer.cancel()
except PendingReduceZ:
    print "Reporte Z"
    printer.close_till()

# Read vat configured in the printer
print "Vat : ", printer.get_rif()
print "##################################################################"

# Read opening date
print "Opening date : ", printer.get_opening_date()
print "##################################################################"

# Read current date from the printes
print "Currente date : ", printer.get_printer_date()
print "##################################################################"

# Read printer general information
print "All printer information : ", printer.get_printer_info()
print "##################################################################"

# Read the till number configured in the printer
print "Till number : ", printer.get_till_number()
print "##################################################################"

# Read the store configured in the printer
print "Store : ", printer.get_store_number()
print "##################################################################"

# Read currency configured in the printer
print "Currency : ", printer.get_currency()
print "##################################################################"

# Read sensors status
print "Sensors status : ", printer.get_sensors_status()
print "##################################################################"

# Read the total sales from the last Z
print "Total sales : ", printer.get_total_day()
print "##################################################################"

# Read the last id
print "Las invoice id : ", printer.get_ccf()
print "##################################################################"

# Read the number of z reports
print "Number of Z reports : ", printer.get_crz()
print "##################################################################"

# Read operations counter
print "Operations counter : ", printer.get_coo()
print "##################################################################"

# Read non fiscal operations counter
print "Non fiscal operations counter : ", printer.get_gnf()
print "##################################################################"

# Read the payments constants thar are stored in the printers
print "Payments constants : ", printer.get_payment_constants()
print "##################################################################"

# Read printer capabilities
print "Capabilities : ", printer.get_capabilities()
print "##################################################################"

# Read tax constants
print "Tax constants : ", printer.get_tax_constants()
print "##################################################################"

