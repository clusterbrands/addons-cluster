import re

from datetime import datetime
from stoqdrivers.enum import PaymentMethodType, TaxType, UnitType
from stoqdrivers.exceptions import (PendingReduceZ,
                                    PendingReadX,
                                    CouponOpenError,
                                    CloseCouponError,)
from decimal import Decimal

from fiscalv import FiscalV
printer = FiscalV(brand='bematech', model='MP4000', device='/dev/ttyUSB0') 

st = printer.get_info_dict()
print st
try:
    p = printer.get_status_printer()
    # printer.close_till()
except CouponOpenError:
    print "Printer has a coupon currently open, lets cancel"
    printer.cancel()
except PendingReduceZ:
    print "Reporte Z"
    printer.close_till()
except Exception, e:
    if printer.has_pending_reduce():
        printer.close_till()
    else:
        raise e
#        printer.set_z_time_limit('08')
#        printer.close_till()
# printer.close_till()
trans = printer.print_trans(345, 347)
print trans
# print "******************************************************"
# trans = trans.split('\n')
# data = {'invoices' : []}
# f = {}
