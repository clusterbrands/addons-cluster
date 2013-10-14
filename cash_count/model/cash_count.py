import time
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc


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
            criteria.append(('role','=','manager'))
        ids = obj.search(cr, uid, criteria, context=context)
        if ids:
            return ids[0]
        else:
            return []

    def wkf_action_open(self, cr, uid, ids, context=None):
        context = context or {}
        values = {'opening_date':time.strftime('%Y-%m-%d %H:%M:%S')}
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
                result = {'status':0,'cashier_id':cashier_id}
            else:
                result = {'status':1,'msg':_("You can open only one session at a time")}
        else:
            result = {'status':1,'msg':_("Wrong user name or password")}
        return result

    def close_session(self, cr, uid, session_id, employee_id, context=None):
        

    _columns = {
        'session_id': fields.many2one('pos.session', 'Pos Session', required=True),
        'cashier_id': fields.many2one('hr.employee', 'Cashier', required=True),
        'opening_date': fields.datetime('Opening Date', readonly=True),
        'closing_date': fields.datetime('Closing Date', readonly=True),
        'state': fields.selection(SESSION_STATE, 'Status',
                                  required=True, readonly=True,
                                  select=1),
    }

    _defaults = {
        'state': 'opened',
    }
