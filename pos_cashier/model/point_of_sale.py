from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.addons.point_of_sale.point_of_sale import pos_session

class pos_session(osv.Model):
    _inherit = 'pos.session'
       
    def close(self, cr, uid, ids, context=None):
        context = context or {}
        obj = self.browse(cr, uid, ids[0], context=context)
        context["session_id"] = obj.id
        context["close"] = True
        return {
            'name': "Select Cashier",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pos.cashier.session.opening',
            'target' : 'new',
            'view_id': False,
            'context':context,
        }
    
    
    def cashier_selected(self, cr, uid, ids, context=None):
        context = context or {}
        session = self.browse(cr, uid, ids[0], context=context);
        if session.cashier_id:
            return True
        else:
            return False
                      
    def create(self, cr, uid, values, context=None):
        context = context or {}
        if context.get("cashier_id"):
            values.update({"cashier_id":context.get("cashier_id")})
        return super(pos_session, self).create(cr, uid, values, context=context)
    
    _columns = {
        'cashier_id': fields.many2one('pos.cashier.cashier', 'Cashier'),
    }

