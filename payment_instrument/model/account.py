from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_journal(osv.Model):

    '''
    Open ERP Model
    '''
    _inherit = 'account.journal'
    _columns = {
        'payment_instrument_ids': fields.one2many('payment_instrument.instrument', 'journal_id', 'Payment Instruments'), 
    }
