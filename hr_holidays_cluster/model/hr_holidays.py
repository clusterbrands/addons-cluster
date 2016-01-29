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

from openerp.osv import fields, osv

class hr_holidays(osv.osv):
	_inherit = "hr.holidays.status"

	_columns = {
		'holidays_leave': fields.boolean('Holidays Leave'),
		'salary_rule_id': fields.many2one('hr.salary.rule', 'Salary Rule', help="Rule of salary to calculate the number of days of enjoyment according to LOTTT"), 
	}

	_sql_constraints = [
        ('holidays_leave_unique', 'unique(holidays_leave)', 
         "A holidays leave already exists!"),
    ]

class hr_holidays(osv.osv):
	_inherit = 'hr.holidays'

	def onchange_status(self, cr, uid, ids, holiday_status_id, context=None):
		result = {}
		if holiday_status_id:
			status = self.pool.get('hr.holidays.status').browse(cr, uid, holiday_status_id, context=context)
			result['value'] = {
				'holidays_leave': status.holidays_leave
			}
		return result

	_columns = {
		'contract_id':fields.many2one('hr.contract', 'Contract', required=True), 
		'holidays_leave': fields.related('holiday_status_id','holidays_leave', type='boolean', relation='hr.holidays.status', string='Holidays Leave'), 
	}