from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc

class pos_cashier_session_opening(osv.osv_memory):
    _name = 'pos.cashier.session.opening'
    
    def default_get(self, cr, uid, fieldnames, context=None):
        context = context or {}
        values = {}
        if context.get("session_id"):
            session_id = context.get("session_id")
            session =self.pool.get("pos.session").browse(cr, uid, session_id, 
                                                         context=context)            
            values.update(
                {"cashier_id":session.cashier_id.id,"session_id":session_id},
            )  
        return values
    
    def open_session_cashier(self, cr, uid, ids, context=None):
        context = context or {}
        wizard = self.browse(cr, uid, ids[0], context=context)
        obj = self.pool.get("pos.cashier.cashier")
        cashier = obj.browse(cr, uid, wizard.cashier_id.id, context=context) 
        if wizard.password == cashier.password:
            context["cashier_id"] = cashier.id
            obj = self.pool.get("pos.session.opening")
            active_ids = context.get("active_ids")      
            return obj.open_session_cb(cr, uid, active_ids, context=context)
        else:
            raise osv.except_osv("Error", 
                                  _("wrong cashier or password!"))   
                                  
    def open_existing_session_cashier(self, cr, uid, ids, context=None):
        context = context or {}
        wf_service = netsvc.LocalService("workflow")
        wizard = self.browse(cr, uid, ids[0], context=context)
        cashier = wizard.session_id.cashier_id
        if wizard.password == cashier.password:
            obj = self.pool.get("pos.session.opening")
            active_ids = context.get("active_ids")
            session_id = context.get("session_id")
            session_obj = self.pool.get("pos.session");
            session = session_obj.browse(cr, uid, session_id, context=context)
            if not context.get("close"):
                return obj.open_ui(cr, uid, active_ids, context=context)
            else:
                wf_service.trg_validate(uid, 'pos.session', session.id, 'close', cr)
                return {
                    'name': "Your Session",
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'pos.session.opening',
                    'target':'inline',
                }                    
        else:
            raise osv.except_osv("Error", 
                                  _("wrong cashier or password!"))   
  
    _columns = {
        'session_id' : fields.many2one('pos.session', 'PoS Session'),
        'cashier_id': fields.many2one('pos.cashier.cashier', 'Cashier',
                                       required=True),
        'password':fields.char(string="Password", size=50, 
                               required=True),
    }
