from openerp.osv import osv, fields
from openerp.tools.translate import _


class pos_session(osv.Model):
    _inherit = 'pos.session'

    def _compute_current_session(self, cr, uid, ids, fieldnames, args, context=None):
        context = context or {}
        result = {}
        obj = self.pool.get('cash.count.cashier.session')
        for record in self.browse(cr, uid, ids, context=context):
            c = [('session_id', '=', record.id), ('state', '=', 'opened')]
            session_ids = obj.search(cr, uid, c, context=context)
            if session_ids:
                result[record.id] = session_ids[0]

        return result

    _columns = {
        'cashier_session_id': fields.function(_compute_current_session,
                                              type='many2one',
                                              relation='cash.count.cashier.session',
                                              string='Current Cashier Session'),
        'cashier_session_ids': fields.one2many('cash.count.cashier.session',
                                               'session_id', 'Cashier Sessions',
                                               required=False),
        'cashier_id': fields.related('cashier_session_id', 'cashier_id',
                                     type='many2one', 
                                     relation='hr.employee',
                                     string='Current Cashier'),


    }
