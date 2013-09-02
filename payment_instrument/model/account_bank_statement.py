from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _

from osv import osv
from osv import fields

class account_bank_statement(osv.Model):
    _inherit = 'account.bank.statement'
    _columns = {
            'code':fields.related('instrument_id', 'code', 'Code',
                help="""Reference Code of Payment Instrument"""),
            'instrument_id':fields.many2one('payment_instrument.instrument',
                'Payment Instrument', help="""Payment Instrument linked to Statement"""),
    }
