"""
This script tests some printer functinoalities, 
only those wich envolve printing a document
"""
import sys, os!
sys.path.append(os.path.abspath('..'))

from datetime import datetime
from stoqdrivers.enum import PaymentMethodType, TaxType, UnitType
from stoqdrivers.exceptions import (PendingReduceZ,
                                    PendingReadX,
                                    CouponOpenError,
                                    CloseCouponError,)
from decimal import Decimal
from time import sleep
from fiscalv import FiscalV
from invoice import fvInvoice

# Declare printer instance with proper configuration
print "Creating instance"
printer = FiscalV(brand='bematech', model='MP4000', device='/dev/ttyUSB0')

# Get printer status and catch any exception just to be sure we can print later
print "Trying to get printer status"
try:
    p = printer.get_status_printer()
except CouponOpenError:
    print "Printer has a coupon currently open, lets cancel"
    printer.cancel()
except PendingReduceZ:
    print "Reporte Z"
    printer.close_till()

# Generate Z report
print "Generating Z report"
printer.close_till()
sleep(10)
# Generate X report
print "Generating X report"
printer.open_till()

# Create an invoice, fisrt we must instantiate fvInvoice class
invoice = fvInvoice()

# identify the customer
invoice.identify_customer(  customer_name    = 'Jose Martinez',
                            customer_address = 'San Antonio', 
                            customer_id      = 'V12345678')

# Add invoice lines
# This line with volume unit and tax
invoice.add_item(   item_code        = 'COD01', 
                    item_description = 'Product with volume and tax',
                    item_price       = 0.01,
                    taxcode          = '12',
                    items_quantity   = 1, 
                    unit             = UnitType.LITERS,
                    discount         = Decimal("0.0"))

# This line with weight unit and tax excempt
invoice.add_item(   item_code        = 'COD02', 
                    item_description = 'Product with weight and tax',
                    item_price       = 0.01,
                    taxcode          = 'FF',
                    items_quantity   = 2, 
                    unit             = UnitType.WEIGHT,
                    discount         = Decimal("0.0"))

# This line with meters unit and tax excempt
invoice.add_item(   item_code        = 'COD03', 
                    item_description = 'Product with meters and tax',
                    item_price       = 0.01,
                    taxcode          = '11',
                    items_quantity   = 3, 
                    unit             = UnitType.METERS,
                    discount         = Decimal("0.0"))

# This line with empty unit and none tax
invoice.add_item(   item_code        = 'COD04', 
                    item_description = 'Product with no unit and none tax',
                    item_price       = 0.01,
                    taxcode          = 'NN',
                    items_quantity   = 4, 
                    unit             = UnitType.EMPTY,
                    discount         = Decimal("0.0"))

# This line with custom unit and tax
invoice.add_item(   item_code        = 'COD05', 
                    item_description = 'Product with custom unit and tax',
                    item_price       = 0.01,
                    taxcode          = '04',
                    items_quantity   = 5, 
                    unit             = UnitType.CUSTOM,
                    unit_desc        = "DC",
                    discount         = Decimal("0.0"))

# Add payments 
# Cash
invoice.add_payment(payment_method = '01',
                    payment_value  = Decimal(0.1))
# Debit card
invoice.add_payment(payment_method = '02',
                    payment_value  = Decimal(0.07))

# Print the invoice
print "Let's try to print the invoice"
try:
    printer.print_invoice(invoice.get_dict())
except CouponOpenError:
    print "Printer has a coupon currently open, lets cancel"
    printer.cancel()
except PendingReduceZ:
    print "Reporte Z"
    printer.close_till()
except CloseCouponError as e:
    print "Could not close the coupon..."

# Print a credit note
# Create an invoice, fisrt we must instantiate fvInvoice class
credit_note = fvInvoice()

# identify the customer
credit_note.identify_customer(  customer_name    = 'Jose Martinez',
                            customer_address = 'San Antonio', 
                            customer_id      = 'V12345678')

# Add credit note lines
# This line with volume unit and tax
credit_note.add_item(   item_code        = 'COD01', 
                    item_description = 'Product with volume and tax',
                    item_price       = 0.01,
                    taxcode          = '12',
                    items_quantity   = 1, 
                    unit             = UnitType.LITERS,
                    discount         = Decimal("0.0"))

# This line with weight unit and tax excempt
credit_note.add_item(   item_code        = 'COD02', 
                    item_description = 'Product with weight and tax',
                    item_price       = 0.01,
                    taxcode          = 'FF',
                    items_quantity   = 2, 
                    unit             = UnitType.WEIGHT,
                    discount         = Decimal("0.0"))

# This line with meters unit and tax excempt
credit_note.add_item(   item_code        = 'COD03', 
                    item_description = 'Product with meters and tax',
                    item_price       = 0.01,
                    taxcode          = 'FF',
                    items_quantity   = 3, 
                    unit             = UnitType.METERS,
                    discount         = Decimal("0.0"))

# This line with empty unit and none tax
credit_note.add_item(   item_code        = 'COD04', 
                    item_description = 'Product with no unit and none tax',
                    item_price       = 0.01,
                    taxcode          = 'NN',
                    items_quantity   = 4, 
                    unit             = UnitType.EMPTY,
                    discount         = Decimal("0.0"))

# This line with custom unit and tax
credit_note.add_item(   item_code        = 'COD05', 
                    item_description = 'Product with custom unit and tax',
                    item_price       = 0.01,
                    taxcode          = '12',
                    items_quantity   = 5, 
                    unit             = UnitType.CUSTOM,
                    unit_desc        = "DC",
                    discount         = Decimal("0.0"))

# Print the credit note
print "Let's try to print the credit note"
try:
    printer.print_credit_note(credit_note.get_dict())
except CouponOpenError:
    print "Printer has a coupon currently open, lets cancel"
    printer.cancel()
except PendingReduceZ:
    print "Reporte Z"
    printer.close_till()
except CloseCouponError as e:
    print "Could not close the coupon..."

# Print day transactions
printer.print_trans(datetime.today().strftime('%Y/%m/%d'), datetime.today().strftime('%Y/%m/%d'))

