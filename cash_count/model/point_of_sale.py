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
                                               required=False),
        'reportx_ids': fields.one2many('cash.count.reportx',
                                       'pos_session_id', 'Reports X',
                                        required=False),
        


    }
