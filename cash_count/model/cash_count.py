import time
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc
import openerp.addons.decimal_precision as dp


class cashier_session(osv.Model):

    _name = "cash.count.cashier.session"

    SESSION_STATE = [
        ('opened', 'In Progress'),                    # Signal closing
        ('closed', 'Closed & Posted'),
    ]

    def login(self, cr, uid, username, password, context=None):
        context = context or {}
        obj = self.pool.get('hr.employee')
        criteria = [('username', '=', username), ('password', '=', password)]
        if context.get('manager'):
            criteria.append(('role', '=', 'manager'))
        ids = obj.search(cr, uid, criteria, context=context)
        if ids:
            return ids[0]
        else:
            return False

    def wkf_action_open(self, cr, uid, ids, context=None):
        context = context or {}
        values = {'opening_date': time.strftime('%Y-%m-%d %H:%M:%S')}
        return self.write(cr, uid, ids, values, context=context)

    def open_session(self, cr, uid, session_id, username, password, context=None):
        context = context or {}
        cashier_id = self.login(cr, uid, username, password, context=context)
        if cashier_id:
            c = [('session_id', '=', session_id), ('state', '=', 'opened')]
            session_ids = self.search(cr, uid, c, context=context)
            if len(session_ids) == 0:
                values = {'session_id': session_id, 'cashier_id': cashier_id}
                s_id = self.create(cr, uid, values, context=context)
                session = self.read(cr, uid, s_id, context=context)
                result = {'status': 0, 'session': session}
            else:
                result = {'status': 1, 'msg': _(
                    "You can open only one session at a time")}
        else:
            result = {'status': 1, 'msg': _("Wrong user name or password")}
        return result

    def close_session(self, cr, uid, session_id, context=None):
        context = context or {}
        session = self.browse(cr, uid, session_id, context=context)
        if session.state == 'opened':
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(
                uid, 'cash.count.cashier.session', session_id, 'close', cr)
            return True
        return False

    def wkf_action_close(self, cr, uid, ids, context=None):
        context = context or {}
        values = {'closing_date': time.strftime('%Y-%m-%d %H:%M:%S')}
        values.update({'state': 'closed'})
        return self.write(cr, uid, ids, values, context=context)

    def unlock_session(self, cr, uid, session_id, username, password, context=None):
        context = context or {}
        cashier_id = self.login(cr, uid, username, password, context=context)
        if cashier_id:
            c = [('session_id', '=', session_id),
                 ('state', '=', 'opened'), ('cashier_id', '=', cashier_id)]
            session_ids = self.search(cr, uid, c, context=context)
            if len(session_ids) == 1:
                return True

        return False

    def create(self, cr, uid, values, context=None):
        context = context or {}
        s_obj = self.pool.get('pos.session')
        s_id = values.get('session_id')
        session = s_obj.browse(cr, uid, s_id, context=context)
        values.update({'name': session.sequence_id._next()})
        return super(cashier_session, self).create(cr, uid, values, context=context)

    _columns = {
        'name': fields.char('Cashier Session ID', size=32, required=True, readonly=True),
        'session_id': fields.many2one('pos.session', 'Pos Session', required=True),
        'cashier_id': fields.many2one('hr.employee', 'Cashier', required=True),
        'opening_date': fields.datetime('Opening Date', readonly=True),
        'closing_date': fields.datetime('Closing Date', readonly=True),
        'state': fields.selection(SESSION_STATE, 'Status',
                                  required=True, readonly=True,
                                  select=1),
        'reportx_id': fields.many2one('cash.count.reportx', 'Report X'),
    }

    _defaults = {
        'state': 'opened',
    }

    class reportx (osv.Model):
        _name = "cash.count.reportx"
        _rec_name = 'number'
        _columns = {
            'number': fields.char('Report Number', size=50),
            'date': fields.datetime('Date', readonly=True),
            'cashier_session_id': fields.many2one('cash.count.cashier.session',
                                                  'Cashier Session'),
            'printer_id': fields.many2one('fiscal_printer.printer', 'Printer'),
            'line_ids': fields.one2many('cash.count.reportx.line', 'reportx_id',
                                        'Report Details'),
        }

    class reportx_line(osv.Model):
        _name = "cash.count.reportx.line"

        _columns = {
            'reportx_id': fields.many2one('cash.count.reportx', 'Report X'),
            'statement_id': fields.many2one('account.bank.statement',
                                            'Statement'),
            'journal_id': fields.related('statement_id', 'journal_id',
                                         type='many2one',
                                         relation='account.journal',
                                         string='Journal'),
            'instrument_id': fields.related('statement_id', 'instrument_id',
                                            type='many2one',
                                            relation='payment_instrument.instrument',
                                            string='Instrument'),
            'end_balance': fields.float('Ending Balance',
                                        required=True,
                                        digits_compute=dp.get_precision(
                                            'Account')),
        }
