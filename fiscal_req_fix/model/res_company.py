from openerp.osv import fields, osv

class res_company(osv.osv):
    _inherit = 'res.company'
	
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('vat'):
        	context.update({'vat':vals.get('vat')})
        res = super(res_company, self).create(cr, uid, vals, context=context)
        return res


