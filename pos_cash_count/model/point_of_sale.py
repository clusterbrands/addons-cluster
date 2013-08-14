from openerp.osv import osv, fields
from openerp.tools.translate import _
import time


class pos_session(osv.Model):
    _inherit = 'pos.session'

    def wkf_action_closing_control(self, cr, uid, ids, context=None):
        """
        Prevents that 'balance_end' and 'balance_end_real' must be always
        equal
        """
        return self.write(cr, uid, ids, {'state': 'closing_control', 'stop_at': time.strftime('%Y-%m-%d %H:%M:%S')}, context=context)

    def wkf_action_close(self, cr, uid, ids, context=None):
        """ Enable difference adjusment for bank journals """
        # Close CashBox
        bsl = self.pool.get('account.bank.statement.line')
        for record in self.browse(cr, uid, ids, context=context):
            for st in record.statement_ids:
                if abs(st.difference) > st.journal_id.amount_authorized_diff:
                    # The pos manager can close statements with maximums.
                    if not self.pool.get('ir.model.access').check_groups(cr, uid, "point_of_sale.group_pos_manager"):
                        raise osv.except_osv(_('Error!'),
                                             _("Your ending balance is too different from the theoretical cash closing (%.2f), the maximum allowed is: %.2f. You can contact your manager to force it.") % (st.difference, st.journal_id.amount_authorized_diff))
                if (st.journal_id.type not in ['bank', 'cash']):
                    raise osv.except_osv(_('Error!'),
                                         _("The type of the journal for your payment method should be bank or cash "))
                if st.difference:
                    if st.difference > 0.0:
                        name = _('Point of Sale Profit')
                        account_id = st.journal_id.profit_account_id.id
                    else:
                        account_id = st.journal_id.loss_account_id.id
                        name = _('Point of Sale Loss')
                    if not account_id:
                        raise osv.except_osv(_('Error!'),
                                             _("Please set your profit and loss accounts on your payment method '%s'. This will allow OpenERP to post the difference of %.2f in your ending balance. To close this session, you can update the 'Closing Cash Control' to avoid any difference.") % (st.journal_id.name, st.difference))
                    bsl.create(cr, uid, {
                               'statement_id': st.id,
                               'amount': st.difference,
                               'ref': record.name,
                               'name': name,
                               'account_id': account_id
                               }, context=context)
                getattr(st, 'button_confirm_%s' %
                        st.journal_id.type)(context=context)
        self._confirm_orders(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'state': 'closed'}, context=context)

        obj = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'point_of_sale', 'menu_point_root')[1]
        return {
            'type': 'ir.actions.client',
            'name': 'Point of Sale Menu',
            'tag': 'reload',
            'params': {'menu_id': obj},
        }

    _columns = {
        'statement_ids': fields.one2many('account.bank.statement', 'pos_session_id', 'Bank Statement'),
    }
