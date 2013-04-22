# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 13:53:44 2012

@author: tulio@vauxoo.com
"""
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
from datetime import datetime

_ = stoqdrivers_gettext
log = Logger('fiscalv')

class ParameterChecker():
    def invoice(self, info):
        """
        Check if invoice dictionary has proper indexs
        """
        invoice_fields = ['customer', 'items', 'payments']
        for cf in invoice_fields:
            if not info.has_key(cf): 
                raise CommandParametersError(_('Invoice "%s" not specified'%(cf)))
        return True

    def customer(self, info):
        """
        Check if customer dictionary has proper indexs
        """
        customer_fields = ['name', 'address', 'vat']
        for cf in customer_fields:
            if not info.has_key(cf):
                raise CommandParametersError(_('Customer "%s" not specified'%(cf)))
            if len(info[cf]) < 3:
                raise CommandParametersError(_('Customer "%s" too short'%(cf)))
        return True

    def items(self, info):
        """
        Check if items dictionary has proper indexs 
        and values are correct
        """
        items_fields = ['code', 'price', 'count', 'tax', 'unit_type', 'description']
        for it in info:
            for cf in items_fields:
                if not it.has_key(cf): 
                    raise CommandParametersError(_('Item "%s" not specified'%(cf)))
            if isinstance(it['code'], str) and len(it['code']) < 2:
                raise CommandParametersError(_('Item "code (%s)" too short'%(it['code'])))
            elif len(str(it['code'])) < 2:
                raise CommandParametersError(_('Item "code (%s)" too short'%(it['code'])))
            if isinstance(it['description'], str) and len(it['description']) < 2:
                raise CommandParametersError(_('Item "description (%s)" invalid or too short'%(it['description'])))

            self._float(it['price'])
            self._float(it['count'])
            if float(it['price']) == 0.0:
                raise CommandParametersError(_('Item price cannot be 0'))
            if float(it['count']) <= 0.0:
                raise CommandParametersError(_('Item count cannot be <= 0'))
        return True
        
    def payments(self, info, methods):
        items_fields = ['type', 'amount']
        if len(info) == 0:
            raise CommandParametersError(_('No payments'))
        for i in info:
            for cf in items_fields:
                if not i.has_key(cf): 
                    raise CommandParametersError(_('Payment "%s" not specified'%(cf)))
            has = False
            for cf in methods:
                if i['type'] == cf[0]:
                    has = True
            if not has:
                raise CommandParametersError(_('Payment "%s" not suported'%(i['type'])))
            self._float(i['amount'])
        return True
    
    def _integer(self, number):
        """
        Check if a string is a proper integer number
        """
        n = str(number)
        if not re.search(r'^[0-9]{1,}$', n):
            raise ValueError(_('Value (%s) is not an integer'%(n)))
        return True

    def _float(self, number):
        """
        Check if a string is a proper float number
        """
        n = str(number)
        if not re.search(r'^[0-9]{1,}(\.[0-9]{1,}|)$', n):
            raise ValueError(_('Value (%s) is not a float'%(n)))
        return True

class ParseConfigFile():
    def __init__(self, file_name):
        if not os.path.exists(file_name):
            raise IOError("%s does not exits"%(file_name))
        if not os.path.isfile(file_name):
            raise IOError("%s is not a file"%(file_name))
        config = ConfigParser.ConfigParser()
        config.readfp(open(file_name))
        self._port = config.get('printer', 'port')
        self._brand = config.get('printer', 'brand')
        self._model = config.get('printer', 'model')
        
    def get_config_dict(self):
        return {'port' : self._port, 'brand' : self._brand, 'model': self._model}
    
    def get_config(self):
        return (self._port, self._brand, self._model)

class FiscalV(FiscalPrinter):
    _checker = ParameterChecker()
    def __init__(self, brand=None, model=None, device=None, config_file=None,
                 *args, **kwargs):
        if config_file != None:
            config = ParseConfigFile(config_file)
            device, brand, model = config.get_config()
        FiscalPrinter.__init__(self, brand, model, device, config_file, *args,
                             **kwargs)
        self._invoice_dict = {}
#        self._driver._set_fiscal_app('FiscalV developed by Vauxoo J-31752088-2')

    def open_credit_note(self):
        return self._driver.credit_note_open()

    def print_invoice(self, invoice):
        """
        Receive a dictionary with invoice parameters 
        and return invoice fiscal numer
        """
        # check data before sending it to the printer
        self._checker.invoice(invoice)
        self._checker.customer(invoice['customer'])
        self._checker.items(invoice['items'])
        self._checker.payments(invoice['payments'], self.get_payment_constants())
        # identify the customer
        self.identify_customer(invoice['customer']['name'][:30], 
                               invoice['customer']['address'],
                               invoice['customer']['vat'])
        self.get_status_printer()
        try:
            self._driver.coupon_open()
        except CommandError:
            sensors = self.get_sensors_status()
            for s in sensors:
                if sensors[s][1]:
                    raise PrinterError(sensors[s][0])
            
        # add items from invoice
        for item in invoice['items']:
            item_id = self.add_item(item_code = item['code'][:13], 
                                    item_description = item['description'][:29],
                                    item_price = Decimal(item['price']), 
                                    taxcode = item['tax'],
                                    items_quantity = Decimal(item['count']),
                                    unit = item['unit_type'],
                                    unit_desc = item['unit_desc'])
        # before adding pauments we need to totalize the invoice
        if not invoice.has_key('discount'):
            invoice.update({'discount' : '0.0'})
        coupon_total = self.totalize(discount=Decimal(invoice['discount']))

        # add payments
        for payment in invoice['payments']:
            # print 'Pagos ',str(payment['type']), Decimal(payment['amount'])
            self.add_payment(str(payment['type']), Decimal(payment['amount']))

        # Invoice done
        coupon_id = self.close()

        # return invoice fiscal number
        return self.get_ccf()

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
            item_id = self.add_item(item_code = item['code'][:13], 
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
        coupon_id = self.close_credit_note()
        # return invoice fiscal number
        return self.get_ccf()

    def close_credit_note(self, promotional_message=''):
        log.info('coupon_close(promotional_message=%r)' % (
            promotional_message))

        if not self._has_been_totalized:
            raise CloseCouponError(_("You must totalize the coupon before "
                                     "closing it"))
        res = self._driver.coupon_close(
            self._format_text(promotional_message))
        self._has_been_totalized = False
        self.payments_total_value = Decimal("0.0")
        self.totalized_value = Decimal("0.0")
        return res

    def get_rif(self):
        """
        Return rif (vat) configured in the printer
        """
        return self._driver._get_rif().strip()

    def get_opening_date(self):
        """
        Return opening date
        """
        return self._driver._get_opening_date()

    def get_printer_date(self):
        """
        Return actual printer date
        """
        return self._driver._get_printer_date()

    def get_printer_info(self):
        """
        Return printer info: status, date, printed invoices, etc
        """
        return self._driver._get_printer_info()
    
    def get_till_number(self):
        """
        Return till number configured in the printer
        """
        return self._driver._get_till_number()

    def get_store_number(self):
        """
        Return store number configured in the printer
        """
        return self._driver._get_store_number()
        
    def get_currency(self):
        """
        Return configured currency in the printer
        """
        return self._driver._get_currency()

    def get_sensors_status(self):
        """
        Return sensor status: open, paper, etc
        """
        return self._driver._get_printer_sensors()


    def get_status_printer(self):
        """
        Return printer status
        """
        return self._driver._check_error()

    def get_last_z(self):
        
        data = self._driver._get_last_z()
        st = data[0]
        total = bcd2dec(data[1:10])/Decimal(100)
        anulaciones = bcd2dec(data[10:17])/Decimal(100)
        descuentos = bcd2dec(data[17:24])/Decimal(100)
        print "Total ", total
        print "Anulaciones ", anulaciones
        print "Descuentos ", descuentos
        for i in range(16):
            o = 24 + i * 2
            f = o + 2
            print "Desde %s hasta %s"%(o, f)
            n = bcd2dec(data[o:f])/Decimal(100)
            print n

        for i in range(16):
            o = 56 + i * 7
            f = o + 7
            print "Desde %s hasta %s"%(o, f)
            n = bcd2dec(data[o:f])/Decimal(100)
            print n
        exento = bcd2dec(data[175:182])/Decimal(100)
        print "Exento ", exento
        retiradas = bcd2dec(data[189:196])/Decimal(100)
        print "Retiradas ", retiradas
        for i in range(9):
            o = 203 + i * 7
            f = o + 7
            print "Desde %s hasta %s"%(o, f)
            n = bcd2dec(data[o:f])/Decimal(100)
            print n
        iva_total = bcd2dec(data[308:317])/Decimal(100)
        print "Iva total ", iva_total

    def get_info_dict(self):
        """
        Return a dictionary with all printer information
        """
        serial = self.get_serial()
        rif = self.get_rif()
        coo = self.get_coo()
        crz = self.get_crz()
        pc = self.get_payment_constants()
        tc = self.get_printer_date()
        pi = self.get_printer_info()
        sn = self.get_store_number()
        tn = self.get_till_number()
        cr = self.get_currency()
        ps = self.get_sensors_status()
        ut = self._driver._get_uptime()
        ccf = self.get_ccf()
        ret = {'printer_serial'           : serial,
               'company_rif'              : rif,
               'printer_date'             : tc.isoformat(),
               'printer_number_operations': coo,
               'printer_number_zrepots'   : crz,
               'printer_payment_constants': pc,
               'printer_description'      : pi,
               'printer_store'            : sn,
               'printer_till'             : tn,
               'printer_currency'         : cr,
               'printer_sensors'          : ps,
               'printer_last_id'          : ccf,
               'up_time'                  : ut
               }
        return ret
        
    def get_info_json(self):
        """
        Return printer information in json format
        """
        ret = self.get_info_dict()
        return json.dumps(ret)
        
    def has_pending_reduce(self):
        """
        Return true if there is a pending reduce (pending to close till)
        """
        print self._driver._read_register(self._driver.registers.SECOND_TO_TILL)
    
    def set_till_store(self, till, store):
        """
        Set Till and Store number for the printer
        """
        self._driver._set_td_ecv(till, store)
    
    def add_payment_method(self, name):
        """
        Add payment method to the printer
        """
        return self._driver._add_payment_method(name)
        
    def get_total_day(self):
        """
        Return the total sale from the last reduce
        """
        return self._driver._get_total_day()

    def get_payments(self):
        """
        This function is in alpha state, should not be used yet
        """
#        values = self._driver._get_totalizers()
#        self._driver.till_read_memory(datetime.date(2012, 9, 1), datetime.date(2012, 9, 21))
        values = self._driver._read_register(self._driver.registers.PAYMENTS)
        print len(values)
#        for i in range(len(values)):
#        print map(hex,map(ord,values))
#        print values[0:16]
        for i in range(20):
            o = i * 16
            f = o + 16
            print "Desde %s hasta %s"%(o, f)
            print values[o:f]
        print "########################################"
        for i in range(16):
            o = i * 7 + 320
            f = o + 7
            print "Desde %s hasta %s"%(o, f)
#            print values[o:f]
            n = bcd2dec(values[o:f])/Decimal(100)
            print n
        n = bcd2dec(values[-9:])/Decimal(100)
        print "Total %s " %(n)

    def get_trans(self, start, end):
        """
        Return a python dict with all operations from a given range
        """
        try:
            start = datetime.strptime(start, '%Y/%m/%d') if isinstance(start, str) else start
            end = datetime.strptime(end, '%Y/%m/%d') if isinstance(end, str) else end
        except ValueError:
            start = int(start)
            end = int(end)
        return self._driver._get_transactions(start, end)

    def print_trans(self, start, end):
        """
        Print all transactions in a given period
        """
        try:
            start = datetime.strptime(start, '%Y/%m/%d') if isinstance(start, str) else start
            end = datetime.strptime(end, '%Y/%m/%d') if isinstance(end, str) else end
        except ValueError:
            start = int(start)
            end = int(end)
        return self._driver._read_transactions(start, end, 'I')
    
    def set_z_time_limit(self, time):
        """
        Set z time limit, still in alfa state
        """
        self._driver._set_z_time_limit(time)

    def add_item(self, item_code, item_description, item_price, taxcode,
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

        return self._driver.coupon_add_item(
            self._format_text(item_code), self._format_text(item_description),
            item_price, taxcode, items_quantity, unit, discount, surcharge,
            unit_desc=self._format_text(unit_desc), refund=refund)

