from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.addons.point_of_sale.point_of_sale import pos_session

class pos_session(osv.Model):
    _inherit = 'pos.session'
    
    POS_SESSION_STATE = [
        ('select_cashier', 'Selecting Cashier'),  
        ('opening_control', 'Opening Control'),  # Signal open
        ('opened', 'In Progress'),                    # Signal closing
        ('validate_cashier', 'Validating Cashier'),
        ('closing_control', 'Closing Control'),  # Signal close
        ('closed', 'Closed & Posted'),
    ]
    
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
            
    def validate_cashier(self, cr, uid, ids, context=None):
        context = context or {}
        session = self.browse(cr, uid, ids[0], context=context)
        context["session_id"] = session.id
        return {
            'name': "Select Cashier",
            'type': 'ir.actions.act_window',
            'res_model': 'pos.cashier.session.opening',
            'target' : 'new',
            'view_id': False,
            'context':context,
        }
   
    def wkf_action_select_cashier(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state' : 'select_cashier'}, context=context)
        
    def wkf_action_validate_cashier(self, cr, uid, ids, context=None):
        #self.write(cr, uid, ids, {'state' : 'validate_cashier'}, context=context)
        context = context or {}
        session = self.browse(cr, uid, ids[0], context=context)
        context['session_id'] = session.id
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

    def create(self, cr, uid, values, context=None):
        context = context or {}
        if context.get("cashier_id"):
            values.update({"cashier_id":context.get("cashier_id")})
        return super(pos_session, self).create(cr, uid, values, context=context)
    
    _columns = {
        'cashier_id': fields.many2one('pos.cashier.cashier', 'Cashier'),
        'state' : fields.selection(POS_SESSION_STATE, 'Status',
                required=True, readonly=True,
                select=1),
    }
    
    _defaults = {
        'state' : 'select_cashier',
    }
