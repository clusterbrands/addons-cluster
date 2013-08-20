from openerp.osv import fields, osv
from openerp.tools.translate import _

from osv import osv
from osv import fields


class instrument(osv.Model):

    '''
    Open ERP Model
    '''
    _name = 'payment_instrument.instrument'
    _description = 'instrument'

    TYPES = [('card', 'Card'), ('ticket', 'Ticket'),
             ('Coupon', 'Coupon'),
             ('giftcard', 'Giftcard')]

    def _get_type(self, cr, uid, ids, field_name, arg, context=None):
        result = dict.fromkeys(ids, "")
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = dict(self.TYPES).get(obj.type)
        return result

    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'type': fields.selection(TYPES,
                                 'Type', select=True, required=True),
        'type_desc': fields.function(_get_type, method=True, type='char', string='Label'), 
        'journal_id': fields.many2one('account.journal', 'Journal'),
        'rule_ids': fields.one2many('payment_instrument.rule', 'instrument_id', 'Rules'), 
    }


class rule(osv.Model):

    '''
    Open ERP Model
    '''
    _name = 'payment_instrument.rule'
    _description = 'rule'

    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'instrument_id': fields.many2one('payment_instrument.instrument', 'Payment Instrument', required=True), 
        'condition_select': fields.selection([('none', 'Always True'), ('range', 'Range')], 'Condition Based on', select=True, required=True),
        'condition_range_min': fields.float('Minimum Range', required=False, help="The minimum amount, applied for this rule."),
        'condition_range_max': fields.float('Maximum Range', required=False, help="The maximum amount, applied for this rule."),
        'amount_select': fields.selection([('percentage', 'Percentage (%)'),
                                          ('fix', 'Fixed Amount')],
                                          'Amount Type', required=True,
                                          help="The computation method for the rule amount."),
        'amount_fix': fields.float('Fixed Amount'),
        'amount_percentage': fields.float('Percentage (%)'),
    }
