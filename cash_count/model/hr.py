from openerp.osv import fields, osv
from openerp.tools.translate import _


class hr_employee(osv.Model):
    _inherit = 'hr.employee'

    def _check_username_uniqueness(self, cr, uid, ids, context=None):
        context = context or {}        
        obj = self.browse(cr, uid, ids, context=context)[0]
        if obj.role == 'cashier':
            user_ids = self.search(cr, uid, [('username', '=', obj.username),
                                             ('id', '!=', ids)])
            return len(user_ids) == 0
        else:
            return True

    _columns = {
        'role': fields.selection([('cashier', 'Cashier'),
                                  ('manager', 'Manager'), ], 'PoS Role',
                                 select=True),
        'username': fields.char('Username', size=64, required=False),
        'password': fields.char('Password', size=64, required=False),
    }

    _defaults = {
        'role': 'none'
    }

    _constraints = [
        (_check_username_uniqueness,
         _("This username already exists"), ['username'])
    ]
