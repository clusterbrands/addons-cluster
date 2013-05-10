#
# Stoqdrivers template driver
#
# Copyright (C) 2007 Async Open Source <http://www.async.com.br>
# All rights reserved
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
# USA.
#

import datetime
import time
import struct
import serial
import pdb
from operator import xor
from decimal import Decimal
from kiwi.python import Settable
from zope.interface import implements

from stoqdrivers.enum import TaxType,UnitType
from stoqdrivers.interfaces import ICouponPrinter
from stoqdrivers.printers.capabilities import Capability
from stoqdrivers.serialbase import SerialBase
from stoqdrivers.translation import stoqdrivers_gettext
from stoqdrivers.exceptions import (HardwareFailure,OutofPaperError,
                                    CouponOpenError,
                                    PrinterError,DriverError,CommandError)


_ = stoqdrivers_gettext


#printer control characters
STX = 0x02
ENQ = 0x05
ETX = 0x03
ACK = 0x06
NAK = 0x15
ETB = 0x17

#printer commands
CMD_ADD_CASHIER = 'PC'
CMD_ADD_HEADER_OR_FOOTER = 'PH'
CMD_SET_PAYMENT_METHOD = 'PE'
CMD_ADD_CUSTOMER_INFO = "i"
CMD_START_CASHIER = '5'
CMD_END_CASHIER = '6'
CMD_COUPON_CANCEL = '7'
CMD_COUPON_CANCEL_ITEM = "k"
CMD_COUPON_SUBTOTAL = "3"
CMD_SET_COUPON_ITEM_BARCODE = 'Y'
CMD_SET_COUPON_BARCODE = 'y'
CMD_SET_FLAG = "PJ"
CMD_SET_TAXES = "PT"
CMD_ADD_DISCOUNT_OR_SURCHAGE_VALUE = "q" 
CMD_ADD_DISCOUNT_OR_SURCHAGE_PERCENT = "p"
CMD_ADD_CREDIT_NOTE_ITEM = 'd' 
CMD_ADD_PAYMENT = '2'
CMD_REDUCE_Z = '10Z'
CMD_REDUCE_X = '10X'

RETRIES_BEFORE_TIMEOUT = 3

s1_keys = [ 
    'casher_number','daily_sale','last_invoice_number',
    'daily_count_invoice','notfis_document_number',
    'notfis_document_count','daily_closing_count',
    'audit_count_report','vat','printer_serial_number',
    'printer_current_time','printer_current_date'
]

s2_keys = [
    'tax_base_subtotal','subtotal_iva','data_dummy','unknow',
    'amount_to_pay','number_of_payments','status'
]

s3_keys = [
    'tax_type_1','tax_value_1','tax_type_2','tax_value_2',
    'tax_type_3','tax_value_3','system_flags'
]

s4_keys = [
    'payment_type_1','payment_type_2','payment_type_3','payment_ype_4',
    'payment_type_5','payment_type_6','payment_type_7','payment_type_8',
    'payment_type_9','payment_type_10','payment_type_11','payment_type_12',
    'payment_type_13','payment_type_14','payment_type_15','payment_type_16',
]

s5_keys = [
    'rif','serial','audit_memory_number','memory_size',
    'memory_free_space','document_count',

]

class SRP350Status(object):
    
    st1_codes = {
    
        0x40:_("Test mode and standby"),
        0x41:_("Test mode and in the middle of a fiscal transaction"),
        0x42:_("Test mode and in the middle of a non fiscal transaction"),
        0x60:_("Fiscal mode and standby"),
        0x68:_("Fiscal mode, out of fiscal memory and waiting"),
        0x61:_("Fiscal mode and in the middle of a fiscal transaction"),
        0x69:_("Fiscal mode, out of fiscal memory and in the middle of"
               "a fiscal transaction"),
        0x62:_("Fiscal mode and in the middle of a non fiscal transaction"),
        0x6A:_("Fiscal mode, out of fiscal memory and in the middle of" 
               "a non fiscal transaction"), 
    }
    
    st2_codes = {
    
        0x08:(HardwareFailure(_("Till Error"))),
        0x41:(OutofPaperError(_("Out of paper"))),
        0x42:(HardwareFailure(_("Mechanical printer error / Paper"))),
        0x43:(HardwareFailure(_("Mechanical printer error / Out of paper"))),       
        0x60:(PrinterError(_("Fiscal Error"))), 
        0x64:(HardwareFailure(_("Fiscal Memory Error"))),  
        0x6C:(HardwareFailure(_("Out of fiscal memory error"))),
        0x48:(HardwareFailure(_("Out of fiscal memory"))),
         
    } 
  
    def __init__(self,value):
        
        for key in self.st2_codes:
            if (key & value) == key:
                print self.st2_codes[key]
                #break
    

def bcd2dec(data):
    return int(''.join(['%02x' % ord(i) for i in data]))

class SRP350(SerialBase):
    
    implements(ICouponPrinter)
    supported = True
    model_name = "Bixolon SRP350 "
    coupon_printer_charset = "ascii"

    def __init__(self, port, consts=None):       
        SerialBase.__init__(self, port)
        self._port.setTimeout(1.5)
        self._port.setWriteTimeout(5)
        self._port.setParity(serial.PARITY_EVEN)
        self.remainder_value = Decimal("0.0")       
        self._reset()
    #
    # Helper methods
    #
    
    def _reset(self):
        self._customer = ""
        self._address = ""
        self._document = ""      
        self._payments = []

    
    def _lrc(self,command):
        return reduce(xor,map(ord,command))
    
    
    def _read_status(self):
        
        self.write(chr(ENQ))
        time.sleep(0.02)
        rt = self.read(5)
        if (len(rt) == 05):
            rt = struct.unpack('ccccc',rt)
            return (ord(rt[1]),ord(rt[2]))
        else:
            return (0,0)
    
     
    def _get_printer_sensors(self): 
        st,err= self._read_status()
        ret = {}        
        ret.update({1 : ("Till Error", err & 0x08 == 0x08)})
        ret.update({2 : ("Out of paper", err & 0x41 == 0x41)})
        ret.update({3 : ("Mechanical printer error / Paper", err & 0x42 == 0x42)})
        ret.update({4 : ("Mechanical printer error / Out of paper", err & 0x43 == 0x43)})
        ret.update({5 : ("Fiscal Error", err & 0x60 == 0x60)})
        ret.update({5 : ("Fiscal Memory Error", err & 0x64 == 0x64)})
        ret.update({6 : ("Out of fiscal memory error", err & 0x6C == 0x6C)})
        ret.update({6 : ("Out of fiscal memory", err & 0x48 == 0x48)})
        return ret 
            
    def read_status1(self):
        
        """   
             
        This command allows to extract information about printer settings as
        serial,registration number and billing data        
       
        """   
             
        reply = self._send_command("S1",response='118s')   
        reply = reply[0][3:100]
        reply = reply.split("\n")      
        s1 = dict(zip(s1_keys,reply))
        return s1
    
    def read_status2(self):
        
        """
        
        This command allows to extract information regarding the 
        status of the Invoice, Credit Note or Debit Note in progress.
        
        """        
        reply = self._send_command("S2",response='79s')   
        reply = reply[0][4:76]        
        reply.replace(' ','')
        reply = reply.split("\n")                 
        s2= dict(zip(s2_keys,reply))
        return s2
    
    def read_status3(self):
        """
        
        This command allows to extract information about the tax rates 
        and state flags.
        
        """        
        reply = self._send_command("S3",response='124s')  
        reply = reply[0][3:122]
        reply = reply.replace('\n','')
        reply = struct.unpack('c4sc4sc4s100s',reply)
        s3= dict(zip(s3_keys,reply))
        return s3
        
    def read_status4(self):
        
        """
        
        This command allows to extract the information related 
        to amounts accrued for each means of payment.        
        
        """
        reply = self._send_command("S4",response='181s')  
        reply = reply[0][3:179]
        reply = reply.split("\n")
        s4 = dict(zip(s4_keys,reply))       
        return s4
        
    def read_status5(self):
        
        """
        
        This command allows to extract information concerning the 
        status of the audit memory.
        Note: Command-only model the Samsung Bixolon SRP-350, SRP-270J,
        OKI M1120, Custom Kube
        
        """
        reply = self._send_command("S5",response='50s')
        reply = reply[0][3:47]
        reply = reply.split("\n")
        s5 = dict(zip(s5_keys,reply))        
        return s5
        
    def read_status8(self):
        reply = self._send_command("S8",response='333s')
        reply = reply[0]
        
    def set_flag(self,flag,value):

        self._send_command(CMD_SET_FLAG,flag.rjust(2,'0'),
                           value.rjust(2,'0'),response="c")
        
    
    def _create_packet(self,command):
        """
        Create a 'pre-package' (command + params, basically) and involves
        it around STX, NB and CS::
           1            2            3     4
        +-----+-------------------+-----+-----+
        | STX |        DATA       | ETX | lrc |
        +-----+-------------------+-----+-----+

        Where:
        STX: 'Transmission Start' indicator byte
        DATA:'Command and parameters'
        ETX: 'Transmission End' indicator byte
        LRC:  XOR from the start of data to ETX
        """   
        lrc = self._lrc(command+chr(ETX))
        return struct.pack('c%dscc' % len(command),chr(STX),command,
                            chr(ETX),chr(lrc))
          
         
    def _check_error(self):
        
        st,err= self._read_status()        
        SRP350Status(err)
        
    
         
    def _send_command(self,cmd,*args,**kwargs):        
        
        if isinstance(cmd,int):
            cmd = chr(cmd)
        
        fmt = ''
        if 'response' in kwargs:
            fmt = kwargs.pop('response')
        
        for arg in args:
            if isinstance(arg, int):
                cmd += chr(arg)
            elif isinstance(arg, str):
                cmd += arg
            else:
                raise NotImplementedError(type(arg))
        
        data = self._create_packet(cmd) 
        self.write(data) 
       
        reply = self._read_reply(struct.calcsize(fmt))        
        
        retval = struct.unpack(fmt, reply)        
        
        if (reply[0] == chr(NAK)):
            raise CommandError(_("Unrecognized command"))
        
        self._check_error()
        return retval
        
    def _read_reply(self, size):
        a = 0
        data = ''
        while True:
            if a > RETRIES_BEFORE_TIMEOUT:
                raise DriverError(_("Timeout communicating with fiscal "
                                    "printer"))

            a += 1
            reply = self.read(size)
            if reply is None:
                continue

            data += reply
            if len(data) < size:

                continue
            
            return data
    
    def _get_amount_to_pay(self):   
        s2 = self.read_status2()
        value = s2['amount_to_pay']
        value = Decimal(value[:-2]+'.'+value[-2:])       
        return value
        
    def _has_pending_reduce():
        return False
    
    def add_cashier(self,id,password,name):
        self._send_command(CMD_ADD_CASHIER,id,password,name,response='c')
        
    
    
    def set_payment_method(self,id,name):
        self._send_command(CMD_SET_PAYMENT_METHOD,id,name,response='c')
    
       
    #Custom Coupon methods
    
    def _set_tax_rates(self,tax_rates):
        
        if len(tax_rates) == 3:
            taxes = {tax.get('code'):tax.get('value') for tax in tax_rates}
            vcodes = set(['!','#','"'])
            if vcodes.difference(set(taxes.keys())) == ():
                data = ("2%05.2f2%05.2f2%05.2f") % (taxes.get('!'),
                        taxes.get('"'),taxes.get('#'))
                data = data.replace(".","")
                self._send_command(CMD_SET_TAXES,data,response='c')
            else:
                raise DriverError(_("This tax codes is not supported from "
                                    "the current printer"))
        else:
            raise DriverError(_("You need to specify the value of "
                                "the three taxes"))
        return True
        
    def set_coupon_header_or_footer(self,id,message):
        self._send_command(CMD_ADD_HEADER_OR_FOOTER,id,message,response='c')
        
    
    def has_open_coupon(self):
        return (self._get_amount_to_pay() <> 0)
        
    def start_cashier(self,password):
        self._send_command(CMD_START_CASHIER,password,response='c') 
    
    def end_cashier(self):
        self._send_command(CMD_END_CASHIER,response='c') 
    
    def _coupon_subtotal(self):
        self._send_command(CMD_COUPON_SUBTOTAL,response='c')
    
    def get_last_coupon_number(self):
        s1 = self.read_status1() 
        return s1['last_invoice_number']    
    
    def coupon_set_item_barcode(self,code):           
        self._send_command(CMD_SET_COUPON_ITEM_BARCODE,code,response='c')
    
    def coupon_set_barcode(self,code):
        self._send_command(CMD_SET_COUPON_BARCODE,code,response='c')
    
    #
    # This implements the ICouponPrinter Intcode,descriptionerface
    #
    # Coupon methods    
   
    
    def coupon_is_customer_idCouponentified(self):
        """ Returns True, if the customer have already been identified,
        False otherwise.
        """
        return ((self._customer and self._address and self._document ) and
                True or False)
    
    def coupon_identify_customer(self,customer, address, document):
        self._customer = "Cliente: "+customer
        self._address =  "Direccion: "+address
        self._document = "Cedula/RIF: "+document      

    def coupon_open(self):
   
        #if not (self.has_open_coupon):
        self._reset        
        self._send_command(CMD_ADD_CUSTOMER_INFO,("%02d%-40s") % (0,self._customer),response='c')
        self._send_command(CMD_ADD_CUSTOMER_INFO,("%02d%-40s") % (1,self._address ),response='c')
        self._send_command(CMD_ADD_CUSTOMER_INFO,("%02d%-40s") % (2,self._document),response='c')

        #else:
        #    raise CouponOpenError(_("Coupon already is open"))

    def coupon_cancel(self):
        self._send_command(CMD_COUPON_CANCEL,response='c')
        self.reset()
        
    def coupon_close(self, message):  

        coupon_number = self.get_last_coupon_number()
        for payment in self._payments:
            data = ('%2s%013.2f' % (payment['payment_method'],
                    payment['value']))
            data = data.replace(".","")

            self._send_command(CMD_ADD_PAYMENT,data,response='c')        
              
        return coupon_number
        

    def coupon_add_item(self, code, description, price, taxcode,
                        quantity=Decimal("1.0"), unit=UnitType.EMPTY,
                        discount=Decimal("0.0"), surchage=Decimal("0.0"),
                        unit_desc="",refund = False):
                                         
        data = ("%011.2f%09.3f%-10s%-30s") %(float(price),
                                            float(quantity),
                                            code,description)
        data = data.replace(".","")
        self._send_command(taxcode,data,response='c')         
        if (discount):
            self._send_command(CMD_ADD_DISCOUNT_OR_SURCHAGE_PERCENT,"-",
                              str(discount),response='c')
        elif(surchage):
            self._send_command(CMD_ADD_DISCOUNT_OR_SURCHAGE_PERCENT,"+",
                              str(surchage),response='c')
        return code

    def coupon_cancel_item(self, item_id):
        self._send_command(CMD_COUPON_CANCEL_ITEM,response='c')

    def coupon_add_payment(self, payment_method, value, description):
        
        self._payments.append({'payment_method':payment_method,'value':value})
        self.remainder_value -= value        
        if self.remainder_value < 0.0:
            self.remainder_value = Decimal("0.0")
        return self.remainder_value
        
    def coupon_totalize(self, discount, surchage, taxcode):
        
        #self._coupon_subtotal()
        totalized_value = self._get_amount_to_pay()
        if (discount):
            self._send_command(CMD_ADD_DISCOUNT_OR_SURCHAGE_VALUE,"-",discount,response='c')
            totalized_value = self._get_amount_to_pay()
        elif(surchage):
            self._send_command(CMD_ADD_DISCOUNT_OR_SURCHAGE_VALUE,"+",surchage,response='c')
            totalized_value = self._get_amount_to_pay()        
        self.remainder_value = totalized_value
        return totalized_value        
        
    #Credit Note Methods
    
    def credit_note_open(self):
        self.coupon_open()

    def credit_note_add_item(self, code, description, price, taxcode,
                        quantity=Decimal("1.0"), unit=UnitType.EMPTY,
                        discount=Decimal("0.0"), surchage=Decimal("0.0"),
                        unit_desc="",refund = False):                        

        data = ("%1s%011.2f%09.3f%-10s%-30s") %(taxcode,float(price),
                                          float(quantity),
                                          code,description)
        data = data.replace(".","")
        self._send_command(CMD_ADD_CREDIT_NOTE_ITEM,data,response='c')
        if (discount):
            self._send_command(CMD_ADD_DISCOUNT_OR_SURCHAGE_PERCENT,"-",
                              str(discount),response='c')
        elif(surchage):
            self._send_command(CMD_ADD_DISCOUNT_OR_SURCHAGE_PERCENT,"+",
                              str(surchage),response='c')
        return code
        
    def credit_note_cancel(self):
        self.coupon_cancel()
        
    def credit_note_set_item_barcode(self,code):           
        self.coupon_set_item_barcode(code)
        
    def credit_note_set_barcode(self,code):
        self.coupon_set_barcode(code)
        
    def credit_note_add_payment(self, payment_method, value, description):
                
        self._payments.append({'payment_method':payment_method,'value':value})
        self.remainder_value -= value        
        if self.remainder_value < 0.0:
            self.remainder_value = Decimal("0.0")
        return self.remainder_value
        
    def credit_note_close(self, message):   
        for payment in self._payments:
            data = ('%2s%013.2f' % (payment['payment_method'],
                    payment['value']))
            data = data.replace(".","")
            self._send_command(CMD_ADD_PAYMENT,data,response='c')        
    
    # Till / Daily flow
    
    def setup(self):
        pass
    def summarize(self):
        self._send_command(CMD_REDUCE_X,response='c')
    
    def open_till(self):
        self.summarize()    

    def close_till(self, previous_day):
        self._send_command(CMD_REDUCE_Z,response='c')

    def till_add_cash(self, value):
        # Suprimento
        pass

    def till_remove_cash(self, value):
        # Sangria
        pass

    def till_read_memory(self, start, end):
        # Leitura Memory Fiscal data
        pass

    def till_read_memory_by_reductions(self, start, end):
        # Leitura Memory Fiscal reducoes
        pass

    # Introspection

    def get_capabilities(self):
        return dict(
            item_code=Capability(max_len=13),
            item_id=Capability(digits=4),
            items_quantity=Capability(min_size=1, digits=8, decimals=3),
            item_price=Capability(digits=10, decimals=2),
            item_description=Capability(max_len=40),
            payment_value=Capability(digits=12, decimals=2),
            promotional_message=Capability(max_len=40),
            payment_description=Capability(max_len=14),
            customer_name=Capability(max_len=30),
            customer_id=Capability(max_len=28),
            customer_address=Capability(max_len=80),
            add_cash_value=Capability(min_size=0.1, digits=12, decimals=2),
            remove_cash_value=Capability(min_size=0.1, digits=12, decimals=2),
            )
            
    def get_ccf(self):
        s5 = self.read_status5()
        return s5['document_count']

    def get_constants(self):
        return self._consts

    def get_tax_constants(self):
        s3 = self.read_status3()
        constants = []
        constants.append({'code':'!',
            'value':s3['tax_value_1'][:2]+'.'+s3['tax_value_1'][-2:],
            'descripcion':'Tax 1'})
        constants.append({'code':'"',
            'value':s3['tax_value_2'][:2]+'.'+s3['tax_value_2'][-2:],
            'descripcion':'Tax 2'})
        constants.append({'code':'#',
            'value':s3['tax_value_3'][:2]+'.'+s3['tax_value_3'][-2:],
            'descripcion':'Tax 3'})
        constants.append({'code':' ','value':'00.00',
            'descripcion':'Exempt'}))
        return constants

    def get_payment_constants(self):
        methods = []
        return methods

    def get_sintegra(self):
        taxes = []
        taxes.append(('2500', Decimal("0")))
        taxes.append(('1800', Decimal("0")))
        taxes.append(('CANC', Decimal("0")))
        taxes.append(('DESC', Decimal("0")))
        taxes.append(('I', Decimal("0")))
        taxes.append(('N', Decimal("0")))
        taxes.append(('F', Decimal("0")))

        return Settable(
             opening_date=datetime.date(2000, 1, 1),
             serial=self._get_serial(),
             serial_id='001',
             coupon_start=0,
             coupon_end=100,
             cro=230,
             crz=1232,
             coo=320,
             period_total=Decimal("1123"),
             total=Decimal("2311123"),
             taxes=taxes)

    # Device detection, asynchronous

    def query_status(self):
        return 'XXX'

    def status_reply_complete(self, reply):
        return len(reply) == 23

    def get_serial(self):
        s1 = self.read_status1()
        return s1['printer_serial_number']

