# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:34:29 2012

@author: truiz
"""

from decimal import Decimal
from stoqdrivers.enum import PaymentMethodType, TaxType, UnitType

class fvInvoice():
    def __init__(self, trim_description = False, trim_code = False):
        self._trim_description = trim_description
        self._trim_code = trim_code
        self._customer = {}
        self._items = []
        self._payments = []
        self._discount = 0.0
        
    def identify_customer(self, customer_name, customer_address, customer_id):
        self._customer.update({'name'    : customer_name,
                               'address' : customer_address,
                               'vat'     : customer_id})

    def add_item(self, item_code, item_description, item_price, taxcode,
                 items_quantity=Decimal("1.0"), unit=UnitType.EMPTY,
                 discount=Decimal("0.0"), surcharge=Decimal("0.0"),
                 unit_desc=""):
        if isinstance(item_code, bool) or item_code == '':
            item_code = '%010d'%(0)
            

        self._items.append({'code'        : item_code,
                            'description' : item_description,
                            'price'       : item_price,
                            'tax'         : taxcode,
                            'count'       : items_quantity,
                            'unit_type'   : unit,
                            'unit_desc'   : unit_desc})

    def add_payment(self, payment_method, payment_value, payment_description=''):
        for i in range(len(self._payments)):
            if self._payments[i]['type'] == payment_method:
                self._payments[i]['amount'] = float(self._payments[i]['amount']) \
                                                + float(payment_value)
                return True
        self._payments.append({'type'        : payment_method,
                               'amount'      : payment_value,
                               'description' : payment_description})
                               
    def get_dict(self):
        ret = {}
        ret.update({'customer' : self._customer})
        ret.update({'items'    : self._items   })
        ret.update({'payments' : self._payments})
        ret.update({'discount' : self._discount})
        return ret
#    def add_payment(self, payment_method, payment_value, description=''):
#        self._payments.update({'payments' : {}})

