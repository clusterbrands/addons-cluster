from openerp.osv import osv, fields
from openerp.tools.translate import _


class hr_payslip(osv.Model):
    _inherit = 'hr.payslip'
    
    def get_utils_dict(self, cr, uid, payslip_id, context=None):
        context = context or {}
        utils = super(hr_payslip, self).get_utils_dict(cr, uid, payslip_id, context=context)
        return utils
