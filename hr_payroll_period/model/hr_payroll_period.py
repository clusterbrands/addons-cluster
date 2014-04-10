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
import datetime
import calendar
from datetime import date, timedelta
from openerp.osv import osv, fields
from openerp.tools.translate import _


class period_schedule(osv.Model):

    _name = 'hr.payroll.period.schedule'

    def _get_weekly_periods(self,start_date):

        periods = []
        end_date = date(start_date.year, 12, 31)
        if (start_date.month > 1):
            start_date = start_date - timedelta(days=start_date.weekday())
        while start_date + timedelta(days=7-start_date.weekday()) < end_date:
            periods.append({
                'date_start': start_date,
                'date_end': start_date + timedelta(days=6-start_date.weekday())
            })
            start_date = start_date + timedelta(days=7-start_date.weekday())
        periods.append({'date_start':start_date, 'date_end': end_date})
        return periods

    def _get_biweekly_periods(self,start_date):
        periods = []
        end_of_year = date(start_date.year, 12, 31)
        while start_date <= end_of_year:
            if start_date.day <= 15:
                start_date = date(start_date.year, start_date.month, 1)
                end_date = date(start_date.year, start_date.month, 15)
            else:
                start_date = date(start_date.year, start_date.month, 16)
                end_day =  calendar.monthrange(start_date.year, start_date.month)[1]
                end_date = date(start_date.year, start_date.month, end_day)
            periods.append({
                'date_start':start_date, 
                'date_end': end_date,
            })
            start_date = end_date + timedelta(days=1)
        return periods

    def _get_monthly_periods(self,start_date):
        periods = []
        end_of_year = date(start_date.year, 12, 31)
        for month in range(start_date.month, 13):
            end_day =  calendar.monthrange(start_date.year, month)[1]
            periods.append({
                'date_start': date(start_date.year, month, 1), 
                'date_end': date(start_date.year, month, end_day),
            })
        return periods

    def _get_fiscal_period(self, cr, uid, from_date, to_date, fiscalyear, context=None):
        context = context or {}
        obj = self.pool.get('account.period')
        c = [('fiscalyear_id','=',fiscalyear),('date_start','<=',to_date)]
        c.append(('date_stop','>=',to_date))
        return obj.search(cr, uid, c, context=context)


    def create_period(self, cr, uid, ids, context=None):
        context = context or {}
        for obj in self.browse(cr, uid, ids, context=context):
            periods = []
            start_date = datetime.datetime.strptime(obj.start_date, '%Y-%m-%d').date()
            if obj.type == "weekly":
                periods = self._get_weekly_periods(start_date) 
            elif obj.type == "bi-weekly":
                periods = self._get_biweekly_periods(start_date)
            elif obj.type == "monthly":
                periods = self._get_monthly_periods(start_date)
            p_obj = self.pool.get('hr.payroll.period')
            p_ids = p_obj.search(cr, uid, [('schedule_id',"=", obj.id)], context=context)
            p_obj.unlink(cr, uid, p_ids, context=context)
            for i in range(0,len(periods)):
                date_start = periods[i].get('date_start')
                date_end =  periods[i].get('date_end')
                period_id = self._get_fiscal_period(cr, uid, date_start, date_end, obj.fiscalyear_id.id)
                if len(period_id) ==  1:
                    values = {
                        'name': "Period "+str(i+1).rjust(2,'0') + "/" + str(start_date.year),
                        'type': obj.type,
                        'schedule_id': obj.id,
                        'date_start': date_start,
                        'date_end': date_end,
                        'fiscal_period_id': period_id[0],
                    }
                    p_id = p_obj.create(cr, uid, values, context=context)
                    if i == 0:
                        wkf_service = netsvc.LocalService('workflow')
                        wkf_service.trg_validate(uid, 'hr.payroll.period', p_id, 'activate', cr)

                else:
                    osv.except_osv(_('Error!'),_("Fiscal period has not found"))

    _columns = {
        'name': fields.char('Description', size=256, required=True),
        'type': fields.selection([
            ('weekly', 'Weekly'),
            ('bi-weekly', 'Bi-weekly'),
            ('monthly', 'Monthly'),
            # ('bi-monthly', 'Bi-monthly'),
            # ('quarterly', 'Quarterly'),
            # ('semi-annually', 'Semi-annually'), 
            # ('annually', 'Annually'),                      
        ],    'Type', select=True, required=True),
        'start_date': fields.date('Initial Period Start Date', required=True),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year', required=True),
        'paydate_biz_day': fields.boolean('Pay Date on a Business Day', required=False),
        'journal_id': fields.many2one('account.journal', 'Salary Journal', required=True),
        'period_ids':fields.one2many('hr.payroll.period', 'schedule_id', 'Periods'),
        'contract_ids':fields.one2many('hr.contract', 'schedule_id', 'Contracts', required=False), 
    }


class period(osv.Model):

    _name = 'hr.payroll.period'

    PERIOD_STATES = [
       ('open', 'Open'),
       ('actived', 'Active'),
       ('confirmed', 'Confirmado'),
       ('paid', 'Paid'),
       ('closed', 'Closed'),
    ]

    _columns = {
        'name': fields.char('Description', size=255, required=True),
        'schedule_id': fields.many2one('hr.payroll.period.schedule',
                                       'Payroll Period Schedule',
                                       required=True, ondelete="cascade"),
        'date_start': fields.date('Start Date', required=True),
        'date_end': fields.date('End Date', required=True),
        'fiscal_period_id': fields.many2one('account.period', 'Fiscal Period', required=True),
        'payslip_ids': fields.one2many('hr.payslip', 'payperiod_id', 'Payslips'),
        'state': fields.selection(PERIOD_STATES, 'State', select=True, readonly=True),
    }

    _defaults = {  
        'state': 'open',  
    }

    def list_fiscal_periods(self, cr, uid, context=None):
        ids = self.pool.get('account.period').search(cr,uid,[])
        return self.pool.get('account.period').name_get(cr, uid, ids, context=context)

    def list_periods_schedules(self, cr, uid, context=None):
        ids = self.pool.get('hr.payroll.period.schedule').search(cr,uid,[])
        return self.pool.get('hr.payroll.period.schedule').name_get(cr, uid, ids, context=context)

    def wkf_action_actived(self, cr, uid, ids, context=None):
        context = context or {}
        return self.write(cr, uid, ids, {'state':'actived'})

    def wkf_action_confirmed(self, cr, uid, ids, context=None):
        context = context or {}
        return self.write(cr, uid, ids, {'state':'confirmed'})

    def wkf_action_paid(self, cr, uid, ids, context=None):
        pass

    def wkf_action_closed(self, cr, uid, ids, context=None):
        pass

    
