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
import netsvc
from datetime import datetime, timedelta
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OEDATE_FORMAT
from openerp.addons.hr_payroll_period.model.hr_payroll_period import period


class wizard_payroll_period(osv.osv_memory):
    _name = 'hr.payroll.period.wizard'

    STATUS = [
       ('step1', 'Step 1: Leaves'),
       ('step2', 'Step 2: Payslips'),
       ('step3', 'Step 3: Payments'),
    ]

    def _get_public_holidays(self, cr, uid, context=None):
        context = context or {}
        ids = []
        p_id = context.get('period_id')
        obj = self.pool.get('hr.payroll.period')
        h_obj = self.pool.get('hr.holidays')
        brw = obj.browse(cr, uid, p_id, context=context)
        start = datetime.strptime(
            brw.date_start, OEDATE_FORMAT).date().strftime(OEDATE_FORMAT)
        end = datetime.strptime(
            brw.date_end, OEDATE_FORMAT).date().strftime(OEDATE_FORMAT)
        dom = [
            '|',
            '&',
            ('date_from', '>=', start),
            ('date_from', '<=', end),
            '&',
            ('date_to', '>=', start),
            ('date_to', '<=', end),
        ]
        ids = h_obj.search(cr, uid, dom, context=context)
        return ids

    _columns = {
        'period_id': fields.many2one('hr.payroll.period', 'Payroll Period',
                                     readonly=True),
        # TODO : import time required to get currect date
        'start_date': fields.date('Start Date', readonly=True),
        'end_date': fields.date('End Date', readonly=True),
        'holiday_ids': fields.many2many('hr.holidays', 'hr_holidays_pay_period_rel', 'holiday_id', 'period_id', 'Holidays'),
        'payslip_ids': fields.many2many('hr.payslip', 'hr_payslip_pay_period_rel', 'payslip_id', 'period_id', 'Payslips'),
        'schedule_id':  fields.related('period_id', 'schedule_id',
                                       type="many2one",
                                       relation="hr.payroll.period.schedule",
                                       string='Schedule', readonly=True),
        'fiscal_period_id':  fields.related('period_id', 'fiscal_period_id',
                                            type="many2one",
                                            relation="account.period",
                                            string='Fiscal Period', readonly=True),
        'step': fields.selection(STATUS, 'State', select=True, readonly=True),
        'state': fields.related('period_id', 'state',
                                type="selection",
                                selection=period.PERIOD_STATES,
                                string='State'),
    }

    def default_get(self, cr, uid, fields_list, context=None):
        context = context or {}
        values = dict.fromkeys(fields_list)
        if context.get('period_id'):
            p_id = context.get('period_id')
            obj = self.pool.get('hr.payroll.period')
            brw = obj.browse(cr, uid, p_id, context=context)
            values.update({
                'period_id': p_id,
                'fiscal_period_id': brw.fiscal_period_id.id,
                'schedule_id': brw.schedule_id.id,
                'start_date': brw.date_start,
                'end_date': brw.date_end,
                'holiday_ids': self._get_public_holidays(cr, uid, context=context),
                'step': context.get('step') or 'step1',
                'state': brw.state,
            })
        return values

    def show_step2(self, cr, uid, ids, context=None):
        context = context or {}
        self.write(cr, uid, ids, {'step':'step2'})
        context.update({'step':'step2'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payroll.period.wizard',
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'context': context
        }

    def show_step3(self, cr, uid, ids, context=None):
        context = context or {}
        self.write(cr, uid, ids, {'step':'step3'})
        context.update({'step':'step3'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payroll.period.wizard',
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'context': context
        }

    def show_step1(self, cr, uid, ids, context=None):
        context = context or {}
        self.write(cr, uid, ids, {'step':'step1'})
        context.update({'step':'step1'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payroll.period.wizard',
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'context': context
        }

    def generate_payslips(self, cr, uid, ids, context=None):
        context = context or {}
        import pdb
        pdb.set_trace()
        data = self.browse(cr, uid, ids, context=context)
        obj_emp = self.pool.get('hr.employee')
        ct_id = data.get('contract_type_id')
        #emp_ids = obj_emp.search(cr, uid, [('contract_ids','in',(ct_id))])



