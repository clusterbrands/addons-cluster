from openerp.osv import osv, fields

class invoice(osv.Model):
    _inherit = 'account.invoice' 
    _columns = {
        'printer_serial':fields.char('Printer Serial',size=50,readonly=True),
        'printer_receipt_number':fields.char('Printer Receipt Ref',size=50,readonly=True)
    }
