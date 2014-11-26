from openerp.osv import fields, osv

class res_partner(osv.osv):
    _inherit = 'res.partner'
    def create (self, cr, uid, vals, context=None):
    	context = context or {}
    	if context.get('vat'):
    		vals.update({'vat': context.get('vat')})
    	return super(res_partner, self).create(cr, uid, vals, context=context)

