from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class wizard_reportx(osv.osv_memory):
    _name = "wizard.reportx"

    _columns = {
        'pos_session_id': fields.many2one('pos.session', 'PoS Session'),
        'user_id': fields.many2one('res.users', 'Responsible', readonly=True),
        'cashier_id': fields.many2one('hr.employee', 'Cashier', readonly=True),
        'config_id': fields.many2one('pos.config', 'Point of Sale',
                                     readonly=True),
        'line_ids': fields.one2many('wizard.reportx.line', 'reportx_id',
                                    'Payment Methods', required=False),
    }

    def default_get(self, cr, uid, fieldnames, context=None):
        context = context or {}
        sop_obj = self.pool.get('pos.session.opening')
        sop = sop_obj.browse(
            cr, uid, context.get('active_id'), context=context)
        result = {}
        result['pos_session_id'] = sop.pos_session_id.id
        result['user_id'] = sop.pos_session_id.user_id.id
        result['cashier_id'] = sop.pos_session_id.cashier_id.id
        result['config_id'] = sop.pos_session_id.config_id.id
        return result

    def end_session(self, cr, uid, ids, context=None):
        context = context or {}
        # WARNING Insert here fiscal_printer code to print the report
        data = self.browse(cr, uid, ids[0], context=context)
        lines = []
        for line in data.line_ids:            
            for s in data.pos_session_id.statement_ids:
                if s.journal_id.id == int(line.journal_id) and s.instrument_id.id == line.instrument_id.id:
                    lines.append((0,0,{'statement_id':s.id,'end_balance':line.amount}))
        values = {}
        values['cashier_session_id'] = data.pos_session_id.cashier_session_id.id
        values['line_ids'] = lines
        obj = self.pool.get('cash.count.reportx')
        obj.create(cr, uid, values, context=context)

class wizard_reportx_line(osv.osv_memory):
    _name = "wizard.reportx.line"

    def _get_journals(self, cr, uid, context=None):
        context = context or {}
        result = []
        if context.get('active_id'):
            sop_id = context.get('active_id')
            sop_obj = self.pool.get('pos.session.opening')
            sop = sop_obj.browse(cr, uid, sop_id, context=context)
            for s in sop.pos_session_id.statement_ids:
                result.append((s.journal_id.id, s.journal_id.name))
        return sorted(set(result))

    def onchange_journal(self, cr, uid, ids, journal_id, context=None):
        context = context or {}
        vals = {}
        if journal_id:
            obj = self.pool.get('account.journal')
            journal = obj.browse(cr, uid, journal_id, context=context)
            vals.update({'type': journal.type, 'instrument_id': ''})
        return {'value': vals}

    _columns = {
        'reportx_id': fields.many2one('wizard.reportx', 'Report'),
        'journal_id': fields.selection(_get_journals, 'Journal', required=True),
        'type': fields.char('Type', size=64),
        'instrument_id': fields.many2one('payment_instrument.instrument',
                                         'Payment Instrument'),
        'amount': fields.float('Amount',
                               required=True,
                               digits_compute=dp.get_precision('Account')),
    }
