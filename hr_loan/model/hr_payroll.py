from openerp.osv import osv, fields
from openerp.tools.translate import _


class hr_payslip(osv.Model):
    _inherit = 'hr.payslip'
    
    def _get_loan_ids(self, cr, uid, slip_id, emp_id, context=None):
        context = context or {}
        slip_pool = self.pool.get('hr.payslip')
        slip = slip_pool.browse(cr, uid, slip_id, context=context)
        cr.execute('''SELECT l.id FROM hr_loan AS l
            INNER JOIN hr_payroll_period AS pp ON l.payroll_period_id = pp.id
            WHERE l.employee_id = %s AND l.state = 'approved' AND
            pp.date_start <= %s AND l.balance != l.amount''', [emp_id, slip.date_from]) 
        return [x[0] for x in cr.fetchall()]
        
    def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context):
        context = context or {}
        res = super(hr_payslip, self).get_payslip_lines(cr, uid, contract_ids, payslip_id, context=context)
        slip_obj = self.pool.get('hr.payslip')
        loan_obj = self.pool.get('hr.loan')
        slip = slip_obj.browse(cr, uid, payslip_id, context=context)
        emp_id = slip.employee_id.id
        loan_ids = self._get_loan_ids(cr, uid, payslip_id, emp_id, context=context)
        for loan in loan_obj.browse(cr, uid, loan_ids, context=context):
            rule = next(r for r in res if r['salary_rule_id'] == loan.type_id.rule_id.id)
            rule['amount'] = loan.quota
            rule['name'] += _(' Quota ') + str(len(loan.balance_ids)+ 1) + '/' + str(loan.periods) 
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
        
    
