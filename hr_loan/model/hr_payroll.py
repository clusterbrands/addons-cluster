from openerp.osv import osv, fields
from openerp.tools.translate import _


class hr_payslip(osv.Model):
    _inherit = 'hr.payslip'
    
    def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context):
        context = context or {}
        res = super(hr_payslip, self).get_payslip_lines(cr, uid, contract_ids, payslip_id, context=context)
        import pdb
        pdb.set_trace()
        return res
    #~ def _get_loan_id(self, cr, uid, employee_id, context=None):
        #~ context = context or {}
        #~ cr.execute('''SELECT l.id FROM hr_loan AS l
            #~ INNER JOIN hr_loan_type AS t on l.type_id = t.id  
            #~ WHERE l.employee_id = %s AND l.state = 'approved' AND
            #~ t.affect_payroll = TRUE''',[employee_id])
        #~ res = cr.fetchone()
        #~ return res and res[0] or False
            #~ 
    #~ def get_utils_dict(self, cr, uid, payslip_id, context=None):
        #~ context = context or {}
        #~ slip_pool = self.pool.get('hr.payslip')
        #~ move_line_pool = self.pool.get('account.move.line')
        #~ loan_pool = self.pool.get('hr.loan')
        #~ payslip = slip_pool.browse(cr, uid, payslip_id, context=context)
        #~ emp_id = payslip.employee_id.id
        #~ utils = super(hr_payslip, self).get_utils_dict(cr, uid, payslip_id, context=context)
        #~ loan_id = self._get_loan_id(cr, uid, emp_id, context=context)
        #~ import pdb
        #~ pdb.set_trace()
        #~ return utils
        
    
