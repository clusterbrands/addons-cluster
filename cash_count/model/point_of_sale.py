import time
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

    def create(self, cr, uid, values, context=None):
        context = context or {}
        s_id = super(pos_session, self).create(cr, uid, values, context=context)
        values = self.browse(cr, uid, s_id, context=context)
        proxy = self.pool.get('ir.sequence')
        sequence_values = dict(
            name='Pos Session %s' % values.name,
            padding=5,
            prefix="%s/"  % values.name,
        )
        sequence_id = proxy.create(cr, uid, sequence_values, context=context)
        self.write(cr, uid, s_id, {'sequence_id':sequence_id})
        return s_id

    def unlink(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.sequence_id:
                obj.sequence_id.unlink()
        return super(pos_session, self).unlink(cr, uid, ids, context=context)

    def wkf_action_closing_control(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state' : 'closing_control', 'stop_at' : time.strftime('%Y-%m-%d %H:%M:%S')}, context=context)

    def wkf_action_close(self, cr, uid, ids, context=None):
        """ Enable difference adjusment for bank journals """
        # Close CashBox
        obj = self.pool.get("fiscal_printer.printer")
        printer = obj.get_printer(cr, uid, context=context)
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
                st.write({'balance_end_real' : st.balance_end_x})
                getattr(st, 'button_confirm_%s' %
                        st.journal_id.type)(context=context)

        res = printer.send_command("print_report_z")
        if res:
            self._confirm_orders(cr, uid, ids, context=context)
            data = {'report_z_number':res.get('report_number'),'state' : 'closed'}
            self.write(cr, uid, ids, data, context=context)        
            obj = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'point_of_sale', 'menu_point_root')[1]
            return {
                'type': 'ir.actions.client',
                'name': 'Point of Sale Menu',
                'tag': 'reload',
                'params': {'menu_id': obj},
            }

    _columns = {
        'sequence_id' : fields.many2one('ir.sequence', 'Session IDs Sequence', readonly=True,
            help="This sequence is automatically created by OpenERP but you can change it "\
                "to customize the reference numbers of your sessions"),

        'cashier_session_id': fields.function(_compute_current_session,
                                              type='many2one',
                                              relation='cash.count.cashier.session',
                                              string='Current Cashier Session'),
        'cashier_id': fields.related('cashier_session_id', 'cashier_id',
                                     type='many2one', 
                                     readonly='True',
                                     relation='hr.employee',
                                     string='Current Cashier'),
        'cashier_session_ids': fields.one2many('cash.count.cashier.session',
                                               'session_id', 'Cashier Sessions',
                                               required=False, readonly=True),
        'reportx_ids': fields.one2many('cash.count.reportx',
                                       'pos_session_id', 'Reports X',
                                        required=False, readonly=True),
        'report_z_number': fields.char('Z Report Number', size=56, readonly=True),
    }
