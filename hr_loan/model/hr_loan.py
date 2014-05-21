#!/usr/bin/python
# -*- encoding: utf-8 -*-
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    Author: Cluster Brands
#    Copyright 2013 Cluster Brands
#    Designed By: Jose J Perez M <jose.perez@clusterbrands.com>
#    Coded by: Eduardo Ochoa  <eduardo.ochoa@clusterbrands.com.ve>
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import time
from openerp.osv import osv, fields
from openerp.tools.translate import _

class hr_loan(osv.Model):
    _name = "hr.loan"

    def _get_loan_quota(self, cr, uid, ids, field_name, args, context=None):
        context = context or {}
        res = dict.fromkeys(ids)
        for loan in self.browse(cr, uid, ids, context=context):
            if loan.periods:
                res[loan.id] = (loan.amount / loan.periods) 
            else:
                res[loan.id] = 0.0
        return res

    _columns = {
        'employee_id':fields.many2one('hr.employee', 'Employee', required=True),
        'contract_id':fields.many2one('hr.contract', 'Contract', required=False),
        'payroll_period_id': fields.many2one('hr.payroll.period', 'Start Payperiod'),
        'type_id':fields.many2one('hr.loan.type', 'Type', required=True), 
        'reason':fields.selection([
            ('apartment','Apartment'),
            ('health','Health'),
            ('studies','Studies')
            ], 'Reason', select=True),
        'amount': fields.float('Amount', digits=(16, 2), required=False), 
        'periods': fields.integer('Periods Numbers'), 
        'quota': fields.function(_get_loan_quota, method=True, type='float', string='Quota'), 
        'details': fields.text('Details'),
        'move_id':fields.many2one('account.move', 'Move', required=False, ondelete='cascade'),
        'state':fields.selection([
            ('to_submit','To Submit'),
            ('to_approve','To Approve'),
            ('approved','Approved'),
            ('declined', 'Declined')
            ], 'State', readonly=True),
    }

    def update_quota(self, cr, uid, ids, context=None):
        context = context or {}
        return True

    def onchange_contract(self, cr, uid, ids, contract_id, context=None):
       	context = context or {}
       	domain = [('schedule_id','=',False),('state','in',('open','actived'))]
        obj = self.pool.get('hr.contract')
        if contract_id:
            contract = obj.browse(cr, uid, contract_id, context=context)
            domain[0] = ('schedule_id','=', contract.schedule_id.id)
            return {'domain':{'payroll_period_id': domain}}
        else:
            res = {'payroll_period_id': False}
            return {'domain':{'payroll_period_id': domain}, 'value': res}

    def do_signal_to_approve(self, cr, uid, ids, context=None):
        context = context or {}
        return self.write(cr, uid, ids, {'state':'to_approve'}, context=context)
        
    def do_signal_approved(self, cr, uid, ids, context=None):
        context = context or {}
        line_ids = []
        move_pool = self.pool.get('account.move')
        period_pool = self.pool.get('account.period')
        pp_pool = self.pool.get('hr.payroll.period')
        #CxP
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Payroll')
        timenow = time.strftime('%Y-%m-%d')
        ctx = dict(context or {}, account_period_prefer_normal=True)
        search_periods = period_pool.find(cr, uid, timenow, context=ctx)
        period_id = search_periods[0]
        loan = self.browse(cr, uid, ids, context=context)[0]
        name = _('Loan for %s') % (loan.employee_id.name)
        move = {
            'date': timenow,
            'ref': name,
            'journal_id': loan.type_id.journal_id.id,
            'period_id': period_id,
        }
        debit_line = (0, 0, {
            'name': 'loan',
            'date': timenow,
            'partner_id': loan.employee_id.address_home_id.id,
            'account_id': loan.type_id.debit_account.id,
            'journal_id': loan.type_id.journal_id.id,
            'period_id': period_id,
            'debit': loan.amount,
            'credit': 0.0,
        })
        line_ids.append(debit_line)
        credit_line = (0, 0, {
            'name': 'loan',
            'date': timenow,
            'partner_id': loan.employee_id.address_home_id.id,
            'account_id': loan.type_id.credit_account.id,
            'journal_id': loan.type_id.journal_id.id,
            'period_id': period_id,
            'debit': 0.0,
            'credit': loan.amount,
        })
        line_ids.append(credit_line)
        move.update({'line_id': line_ids})
        move_id = move_pool.create(cr, uid, move, context=context)
        self.write(cr, uid, ids, {'move_id': move_id})
                
        #CxC
        period = loan.payroll_period_id.number
        period_numbers = [p for p in range(period, period + loan.periods)]
        domain = [('number','in', period_numbers)]
        period_ids = pp_pool.search(cr, uid, domain, context=context)
        if len(period_ids) != loan.periods:
            raise osv.except_osv( _('Error!'), _("The number of payroll periods defined does no match with the number of payments installments"))
        i = 1
        for pr in pp_pool.browse(cr, uid, period_ids, context=context):
            line_ids = []
            move = {
                'date': pr.date_end,
                'ref': _('Loan for %s Quote %d') % (loan.employee_id.name,i),
                'journal_id': loan.type_id.journal_id.id,
                'period_id': pr.fiscal_period_id.id,
            }
            debit_line = (0, 0, {
                'name': 'Payment of Quote '+str(i),
                'date_maturity': pr.date_end,
                'partner_id': loan.employee_id.address_home_id.id,
                'account_id': loan.type_id.credit_account.id,
                'journal_id': loan.type_id.journal_id.id,
                'period_id': pr.fiscal_period_id.id,
                'debit': loan.quota,
                'credit': 0.0,
            })            
            credit_line = (0, 0, {
                'name': 'Payment of Quote '+str(i),
                'date_maturity': pr.date_end,
                'partner_id': loan.employee_id.address_home_id.id,
                'account_id': loan.type_id.debit_account.id,
                'journal_id': loan.type_id.journal_id.id,
                'period_id': pr.fiscal_period_id.id,
                'debit': 0.0,
                'credit': loan.quota,
            })
            line_ids.append(debit_line)
            line_ids.append(credit_line)
            move.update({'line_id': line_ids})
            move_id = move_pool.create(cr, uid, move, context=context)
            i+=1
        return self.write(cr, uid, ids, {'state':'approved'}, context=context)

    def do_signal_decline(self, cr, uid, ids, context=None):
        context = context or {}
        return self.write(cr, uid, ids, {'state':'declined'}, context=context)
        
    def check_contract_and_period(self, cr, uid, ids, context=None):
        for brw in self.browse(cr, uid, ids, context=context):
            if not brw.contract_id:
                raise osv.except_osv( _('Error!'), _("You should select a valid contract to approve this loan"))
            if not brw.payroll_period_id:
                raise osv.except_osv( _('Error!'), _("You should select a valid start 'Payperiod' to approve this loan"))
        return True

class hr_loan_type(osv.Model):
    _name = "hr.loan.type"

    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'code': fields.char('Code', size=55, required=True), 
        'max_amount': fields.float('Max. Amount ', digits=(16, 2), required=False), 
        'min_discount': fields.float('Min. Discount ', digits=(16, 2), required=False), 
        'journal_id': fields.many2one('account.journal', 'Journal', required=True), 
        'debit_account':fields.many2one('account.account', 'Debit Account', required=True), 
        'credit_account':fields.many2one('account.account', 'Credit Account', required=True), 
        'affect_payroll':fields.boolean('Payroll', required=False), 
        'affect_holidays':fields.boolean('Holidays', required=False),
        'affect_social_benefits':fields.boolean('Social Benefits', required=False),
        'affect_eventual':fields.boolean('Eventuals', required=False),
        'details': fields.text('Details'), 
    }
