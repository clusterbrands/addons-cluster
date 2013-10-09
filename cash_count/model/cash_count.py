from openerp.osv import osv, fields
from openerp.tools.translate import _


class cashier_session(osv.Model):

    _name = "cash.count.cashier.session"

    SESSION_STATE = [
        ('opened', 'In Progress'),                    # Signal closing
        ('closed', 'Closed & Posted'),
    ]

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
