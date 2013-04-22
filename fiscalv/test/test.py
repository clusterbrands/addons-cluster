# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 09:25:12 2012

@author: truiz
"""
import sys
sys.path.append('../')
from fiscalv import FiscalV

def read_partner_data():
    printer = FiscalV(brand='bematech', model='MP4000', device='/dev/ttyUSB0') 
#    printer.cancel()
#    return
    rd = printer.get_info_dict()
    print 'Dict ', rd
    rj = printer.get_info_json()
    print 'Json ', rj

def print_invoice():
    printer = FiscalV(brand='bematech', model='MP4000', device='/dev/ttyUSB0') 
    invoice = {}
#    if printer.has_pending_reduce(): 
#        print "Pendiente reporte z, generando..."
#        printer.close_till()
    
    invoice.update({'customer': {'name': 'Henrique Romano ', 
                                 'address': 'San Antonio', 
                                 'vat': '1234567890'}
                                 })
    invoice.update({'items': []})
    invoice['items'].append({'code': '987654321', 
                             'description' : 'Papas Fritas',
                             'price': '0.01',
                             'tax' : 'FF',
                             'count' : '1',
                             'unit': UnitType.WEIGHT})
    invoice['items'].append({'code': 'AG00123', 
                             'description' : 'Agua',
                             'price': '0.01',
                             'tax' : 'FF',
                             'count' : '3',
                             'unit': UnitType.LITERS})
    invoice.update({'payments': []})
    invoice['payments'].append({'type':'01', 'amount': '0.02'})
    invoice['payments'].append({'type':'01', 'amount': '0.02'})
    invoice.update({'discount':'0.0'})
    try:
        printer.print_invoice(invoice)
    except CouponOpenError:
        print "Printer has a coupon currently open, lets cancel"
        printer.cancel()
        
    


if __name__ == "__main__":
    print "Test reading printer data ..."
    read_partner_data()
        
    print "Test printing an invoice from a dictionary"
#    print_invoice()
