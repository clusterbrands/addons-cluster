from openerp.osv import osv, fields
from openerp.tools.translate import _


class pos_session_opening(osv.osv_memory):
    _inherit = 'pos.session.opening'

    _columns = {
        'cashier_name': fields.char('Cashier', size=64, readonly=True),
        'session_opened': fields.boolean('Has Open Session', required=False),
    }

    def on_change_config(self, cr, uid, ids, config_id, context=None):
        context = context or {}
        result = super(pos_session_opening, self).on_change_config(
            cr, uid, ids, config_id, context=context)
        values = result.get('value')
        obj = self.pool.get('pos.session')
        session = obj.browse(
            cr, uid, values.get('pos_session_id'), context=context)
        if session.cashier_session_id:
            values.update({'cashier_name': session.cashier_id.name})
            values.update({'session_opened': True})
        else:
            values.update({'session_opened': False})        
        result.update({'value': values})
        return result

