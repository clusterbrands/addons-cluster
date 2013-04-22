from fiscalv import FiscalV
from stoqdrivers.printers.fiscal import FiscalPrinter
from stoqdrivers.translation import stoqdrivers_gettext
from stoqdrivers.exceptions import (CommandParametersError,)
from kiwi.log import Logger
from decimal import Decimal
import json
import re
import os
import ConfigParser
from stoqdrivers.printers.bematech.MP25 import *
from stoqdrivers.printers.bixolon.SRP350 import *
from datetime import datetime
class FiscalX(FiscalV):
    
    def print_credit_note(self, invoice):
        """
        Receive a dictionary with credit note parameters 
        and return invoice fiscal numer
        """
        # check data before sending it to the printer
        self._checker.invoice(invoice)
        self._checker.customer(invoice['customer'])
        self._checker.items(invoice['items'])
        # identify the customer
        self.identify_customer(invoice['customer']['name'][:30], 
                               invoice['customer']['address'],
                               invoice['customer']['vat'])
        self.get_status_printer()
        try:
            self.open_credit_note()
        except CommandError:
            sensors = self.get_sensors_status()
            for s in sensors:
                if sensors[s][1]:
                    raise PrinterError(sensors[s][0])

        # add items from coupon
        for item in invoice['items']:
            item_id = self.add_item_credit_note(item_code = item['code'][:13], 
                                    item_description = item['description'][:29],
                                    item_price = Decimal(item['price']), 
                                    taxcode = item['tax'],
                                    items_quantity = Decimal(item['count']),
                                    unit = item['unit_type'],
                                    unit_desc = item['unit_desc'])
        # before adding payments we need to totalize the coupon
        if not invoice.has_key('discount'):
            invoice.update({'discount' : '0.0'})
        coupon_total = self.totalize(discount=Decimal(invoice['discount']))
        
        print "total "+str(coupon_total)
        # add payments
        for payment in invoice['payments']:
            # print 'Pagos ',str(payment['type']), Decimal(payment['amount'])
            self.add_payment(str(payment['type']), Decimal(payment['amount']))
        coupon_id = self.close_credit_note()
        # return invoice fiscal number
        return self.get_ccf()
    
    def add_item_credit_note(self, item_code, item_description, item_price, taxcode,
                 items_quantity=Decimal("1.0"), unit=UnitType.EMPTY,
                 discount=Decimal("0.0"), surcharge=Decimal("0.0"),
                 unit_desc="", refund = False):
        log.info("add_item(code=%r, description=%r, price=%r, "
                 "taxcode=%r, quantity=%r, unit=%r, discount=%r, "
                 "surcharge=%r, unit_desc=%r)" % (
            item_code, item_description, item_price, taxcode,
            items_quantity, unit, discount, surcharge, unit_desc))

        if self._has_been_totalized:
            raise AlreadyTotalized("the coupon is already totalized, you "
                                   "can't add more items")
        if discount and surcharge:
            raise TypeError("discount and surcharge can not be used together")
        elif unit != UnitType.CUSTOM and unit_desc:
            raise ValueError("You can't specify the unit description if "
                             "you aren't using UnitType.CUSTOM constant.")
        elif unit == UnitType.CUSTOM and not unit_desc:
            raise ValueError("You must specify the unit description when "
                             "using UnitType.CUSTOM constant.")
        elif unit == UnitType.CUSTOM and len(unit_desc) != 2:
            raise ValueError("unit description must be 2-byte sized string")
        if not item_price:
            raise InvalidValue("The item value must be greater than zero")

        return self._driver.credit_note_add_item(
            self._format_text(item_code), self._format_text(item_description),
            item_price, taxcode, items_quantity, unit, discount, surcharge,
            unit_desc=self._format_text(unit_desc), refund=refund)
            
    
