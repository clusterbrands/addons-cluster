from openerp.osv import osv, fields
from openerp.tools.translate import _


class pos_cashier_session_opening(osv.osv_memory):
    _name = 'pos.cashier.session.opening'
    
    def open_session(self, cr, uid, ids, context=None):
        context = context or {}
        wizard = self.browse(cr, uid, ids[0], context=context)
        obj = self.pool.get("pos.cashier.cashier")
        cashier = obj.browse(cr, uid, wizard.cashier_id.id, context=context) 
        if wizard.password == cashier.password:
            return {
                'type' : 'ir.actions.client',
                'name' : _('Start Point Of Sale'),
                'tag' : 'pos.ui',
                'context' : context
            }
        else:
            raise osv.except_osv("Error", 
                                  _("Incorrect cashier or password!"))
    
    _columns = {
        'cashier_id': fields.many2one('pos.cashier.cashier', 'Cashier',
                                       required=True),
        'password':fields.char(string="Password", size=50, 
                               required=True),
    }
