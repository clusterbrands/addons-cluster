from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import logging
import pdb
import time

import openerp
from openerp import netsvc, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product

class pos_config (osv.Model):
    _inherit = 'pos.config' 
    _columns = {
        'country_id': fields.many2one('res.country',string="Country",required=True),
    }
class pos_order(osv.osv):
    _inherit = "pos.order"
    
    def create_from_ui(self, cr, uid, orders, context=None):
        #_logger.info("orders: %r", orders)
        order_ids = []
        for tmp_order in orders:
            order = tmp_order['data']
            order_id = self.create(cr, uid, {
                'name': order['name'],
                'user_id': order['user_id'] or False,
                'session_id': order['pos_session_id'],
                'lines': order['lines'],
                'pos_reference':order['name'],
                'partner_id':order.get('partner_id'),
            }, context)

            for payments in order['statement_ids']:
                payment = payments[2]
                self.add_payment(cr, uid, order_id, {
                    'amount': payment['amount'] or 0.0,
                    'payment_date': payment['name'],
                    'statement_id': payment['statement_id'],
                    'payment_name': payment.get('note', False),
                    'journal': payment['journal_id']
                }, context=context)

            if order['amount_return']:
                session = self.pool.get('pos.session').browse(cr, uid, order['pos_session_id'], context=context)
                cash_journal = session.cash_journal_id
                cash_statement = False
                if not cash_journal:
                    cash_journal_ids = filter(lambda st: st.journal_id.type=='cash', session.statement_ids)
                    if not len(cash_journal_ids):
                        raise osv.except_osv( _('error!'),
                            _("No cash statement found for this session. Unable to record returned cash."))
                    cash_journal = cash_journal_ids[0].journal_id
                self.add_payment(cr, uid, order_id, {
                    'amount': -order['amount_return'],
                    'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'payment_name': _('return'),
                    'journal': cash_journal.id,
                }, context=context)
            order_ids.append(order_id)
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'pos.order', order_id, 'paid', cr)
        return order_ids
