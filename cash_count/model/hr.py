from openerp.osv import fields, osv


class hr_employee(osv.Model):
    _inherit = 'hr.employee'

    def login(self, cr, uid, user, password, context=None):
        context = context or {}
        ids = self.search(
            cr, uid, [('user', '=', user), ('password', '=', password)], context=context)
        if ids:
            return self.read(cr, uid, ids[0], context=context)
        else:
            return {}

    _columns = {
        'cashier': fields.boolean('Is a Cashier', required=False),
        'user': fields.char('User', size=64, required=False),
        'password': fields.char('Password', size=64, required=False),
        'active': fields.boolean('Active', required=False),
        'ean13': fields.char('EAN13 Barcode', size=13),
    }
    _defaults = {
        'active': True,
    }
