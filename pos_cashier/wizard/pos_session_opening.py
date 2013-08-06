from openerp.osv import osv, fields
from openerp.tools.translate import _

class pos_session_opening(osv.osv_memory):
    _inherit = 'pos.session.opening'
    
    def open_session_cashier(self, cr, uid, ids, context=None):
        context = context or {}
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
    def open_existing_session_cashier(self, cr, uid, ids, context=None):
        context = context or {}
        wizard = self.browse(cr, uid, ids[0], context=context)
        context["session_id"] = wizard.pos_session_id.id
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

    
