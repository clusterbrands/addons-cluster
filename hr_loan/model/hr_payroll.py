import time
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
            pp.date_start <= %s AND l.balance != 0''', [emp_id, slip.date_from]) 
        return [x[0] for x in cr.fetchall()]
        
    def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context):        
        context = context or {}
        res = super(hr_payslip, self).get_payslip_lines(cr, uid, contract_ids, payslip_id, context=context)
        slip_obj = self.pool.get('hr.payslip')
        loan_obj = self.pool.get('hr.loan')
        slip = slip_obj.browse(cr, uid, payslip_id, context=context)
        emp_id = slip.employee_id.id
        struct_id = slip.employee_id.contract_id.struct_id
        loan_ids = self._get_loan_ids(cr, uid, payslip_id, emp_id, context=context)
        for loan in loan_obj.browse(cr, uid, loan_ids, context=context):
            try:
                rule = next(r for r in res if r['salary_rule_id'] == loan.type_id.rule_id.id)
                rule['amount'] = loan.quota * -1
                rule['name'] += _(' Quota ') + str(len(loan.balance_ids)+ 1) + '/' + str(loan.periods) 
            except StopIteration as e:           
                raise osv.except_osv(_('Config Error'),_("The salary structure '"+ struct_id.name + "' has no contains salary rules for payment of Loans"))
        return res
    
    def process_sheet(self, cr, uid, ids, context=None):
        context = context or {}
        line_pool = self.pool.get('account.move.line')
        balance_pool = self.pool.get('hr.loan.balance')
        loan_obj = self.pool.get('hr.loan')
        for slip in self.browse(cr, uid, ids, context=context):
            super(hr_payslip, self).process_sheet(cr, uid, [slip.id], context=context)
            loan_ids = self._get_loan_ids(cr, uid, slip.id, slip.employee_id.id, context=context)
            for loan in loan_obj.browse(cr, uid, loan_ids, context=context):
                rule = loan.type_id.rule_id
                line_id = line_pool.search(cr, uid, [('move_id','=',slip.move_id.id),('name','ilike',rule.name)])
                if line_id:
                    line = line_pool.browse(cr, uid, line_id, context=context)[0]
                    vals = {
                        'loan_id': loan.id,
                        'reference': line.name,
                        'date': time.strftime('%Y-%m-%d'),
                        'move_id': line.id,
                    }
                    balance_pool.create(cr, uid, vals, context=context)
                    
        return True
