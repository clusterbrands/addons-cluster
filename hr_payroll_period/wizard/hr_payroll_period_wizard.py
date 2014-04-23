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
        ('step4', 'Step 4: Print Reports'),
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
        'employee_payslips': fields.boolean('Employee Payslips', readonly=True),
        'payslip_details':fields.boolean('Payslip Details', readonly=True), 
        'rule_summary': fields.boolean('Salary Rule Summary', readonly=True),
        'payroll_summary': fields.boolean('Payroll Summary', readonly=True),
        'holiday_ids': fields.many2many('hr.holidays', 'hr_holidays_pay_period_rel', 'holiday_id', 'period_id', 'Holidays'),
        'payslip_ids': fields.related('period_id', 'payslip_ids',
                                      type="one2many",
                                      relation="hr.payslip",
                                      string='Payslips', readonly=True),
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
                'employee_payslips': brw.employee_payslips,
                'payslip_details': brw.payslip_details,
                'rule_summary': brw.rule_summary,
                'payroll_summary': brw.payroll_summary,
                'holiday_ids': self._get_public_holidays(cr, uid, context=context),
                'payslip_ids': [slip.id for slip in brw.payslip_ids],
                'step': context.get('step') or 'step1',
                'state': brw.state,
            })
        return values

    def show_step1(self, cr, uid, ids, context=None):
        context = context or {}
        self.write(cr, uid, ids, {'step': 'step1'})
        context.update({'step': 'step1'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payroll.period.wizard',
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'context': context
        }

    def show_step2(self, cr, uid, ids, context=None):
        context = context or {}
        self.write(cr, uid, ids, {'step': 'step2'})
        context.update({'step': 'step2'})
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
        self.write(cr, uid, ids, {'step': 'step3'})
        context.update({'step': 'step3'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payroll.period.wizard',
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'context': context
        }

    def show_step4(self, cr, uid, ids, context=None):
        context = context or {}
        self.write(cr, uid, ids, {'step': 'step4'})
        context.update({'step': 'step4'})
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
        data = self.browse(cr, uid, ids, context=context)[0]
        slip_ids = []
        obj_slip = self.pool.get('hr.payslip')
        from_date = data.start_date
        to_date = data.end_date
        for contract in data.schedule_id.contract_ids:
            emp = contract.employee_id
            dom = [
                ('employee_id', '=', emp.id),
                ('payperiod_id', '=', data.period_id.id)
            ]
            slip_id = obj_slip.search(cr, uid, dom, context=context)
            s_id = slip_id and slip_id[0] or 0
            slip_data = obj_slip.onchange_employee_id(
                cr, uid, slip_id, from_date, to_date, emp.id, contract_id=False, context=context)
            journal_id = contract.journal_id.id or data.schedule_id.journal_id.id
            res = {
                'employee_id': emp.id,
                'name': slip_data['value'].get('name', False),
                'struct_id': slip_data['value'].get('struct_id', False),
                'contract_id': slip_data['value'].get('contract_id', False),
                'input_line_ids': [(0, s_id, x) for x in slip_data['value'].get('input_line_ids', False)],
                'worked_days_line_ids': [(0, s_id, x) for x in slip_data['value'].get('worked_days_line_ids', False)],
                'payperiod_id': data.period_id.id,
                'journal_id': journal_id,
                'date_from': from_date,
                'date_to': to_date,
            }
            if slip_id:
                obj_slip.write(cr, uid, s_id, res, context=context)
                slip_ids.append(s_id)
            else:
                slip_ids.append(obj_slip.create(cr, uid, res, context=context))
            obj_slip.compute_sheet(cr, uid, slip_ids, context=context)
        return True

    def confirm_payslips(self, cr, uid, ids, context=None):
        context = context or {}
        data = self.browse(cr, uid, ids, context=context)[0]
        obj_slip = self.pool.get('hr.payslip')
        wkf_service = netsvc.LocalService('workflow')
        for slip in data.period_id.payslip_ids:
            wkf_service.trg_validate(
                uid, 'hr.payslip', slip.id, 'hr_verify_sheet', cr)
        wkf_service.trg_validate(
            uid, 'hr.payroll.period', data.period_id.id, 'confirm', cr)
        context.update({'step': 'step3'})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.payroll.period.wizard',
            'type': 'ir.actions.act_window',
            'target': 'inline',
            'context': context
        }

    def print_payslips(self, cr, uid, ids, context=None):
        context = context or {}
        data = self.browse(cr, uid, ids, context=context)[0]
        obj = self.pool.get('hr.payroll.period')
        obj.write(cr, uid, data.period_id.id, {'employee_payslips': True}, context=context)
        self.write(cr, uid, ids,  {'employee_payslips': True}, context=context)
        datas = {
            'ids': [slip.id for slip in data.period_id.payslip_ids],
            'model': 'hr.payslip',
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'payslip.webkit',
            'datas': datas,
        }

    def print_rule_summary(self, cr, uid, ids, context=None):
        context = context or {}
        data = self.browse(cr, uid, ids, context=context)[0]
        obj = self.pool.get('hr.payroll.period')
        obj.write(cr, uid, data.period_id.id, {'rule_summary': True}, context=context)
        self.write(cr, uid, ids,  {'rule_summary': True}, context=context)
        datas = {
            'ids': [slip.id for slip in data.period_id.payslip_ids],
            'model': 'hr.payslip',
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'rule.summary',
            'datas': datas,
        }

    def print_payroll_summary(self, cr, uid, ids, context=None):
        context = context or {}
        data = self.browse(cr, uid, ids, context=context)[0]
        obj = self.pool.get('hr.payroll.period')
        obj.write(cr, uid, data.period_id.id, {'payroll_summary': True}, context=context)
        self.write(cr, uid, ids,  {'payroll_summary': True}, context=context)
        datas = {
            'ids': [slip.id for slip in data.period_id.payslip_ids],
            'model': 'hr.payslip',
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'payroll.summary',
            'datas': datas,
        }

    def print_payslip_details(self, cr, uid, ids, context=None):
        context = context or {}
        data = self.browse(cr, uid, ids, context=context)[0]
        obj = self.pool.get('hr.payroll.period')
        obj.write(cr, uid, data.period_id.id, {'payslip_details': True}, context=context)
        self.write(cr, uid, ids,  {'payslip_details': True}, context=context)
        datas = {
            'ids': [slip.id for slip in data.period_id.payslip_ids],
            'model': 'hr.payslip',
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'paylip.details',
            'datas': datas,
        }

