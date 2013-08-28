from openerp.osv import osv, fields
from openerp.tools.translate import _


class cashier(osv.Model):
    _name = "cash.count.cashier"

    def validate(self, cr, uid, name, password, context=None):
        context = context or {}
        ids =  self.search(cr, uid, [('name','=',name),('password','=',password)], context=context)
        if ids:
            return self.read(cr, uid, ids[0], ['name'], context=context)
        else:
            return {}

    _columns = {
        "name":fields.char(string="Name", size=50, required=True),
        "password":fields.char(string="Password", size=50,
                               required=True),
    }
