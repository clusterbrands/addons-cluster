from openerp.osv import osv, fields
from openerp.tools.translate import _


class pos_session(osv.Model):
    _inherit = 'pos.session'

    _columns = {
        'cashier_session_ids': fields.one2many('cash.count.cashier.session',
                                               'session_id', 'Cashier Sessions',
                                               required=False),
    }
