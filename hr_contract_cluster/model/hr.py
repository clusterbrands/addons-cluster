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
from dateutil.relativedelta import relativedelta
from datetime import datetime

class hr_employee(osv.osv):
    _inherit = "hr.employee"

    def _get_seniority_fnc(self, cr, uid, ids, field_names, args, context=None):
		res = dict.fromkeys(ids, False)
		current_date = datetime.now().date()
		for emp in self.browse(cr, uid, ids, context=context):
			if emp.entry_date:
				entry_date = datetime.strptime(emp.entry_date, "%Y-%m-%d")
				diff = relativedelta(current_date, entry_date).years
				res[emp.id] = diff
		return res	

    _columns = {
    	'entry_date': fields.date("Entry Date"),
    	'seniority': fields.function(_get_seniority_fnc, method=True, type='integer', store=True, string='Seniority'),
    }

    def _check_entry_date(self, cr, uid, ids, context=None):
    	current_date = datetime.now().date()
    	for emp in self.browse(cr, uid, ids, context=context):
    		if current_date < datetime.strptime(emp.entry_date, "%Y-%m-%d").date():
    			return False
    	return True

    _constraints = [(_check_entry_date, "The entry date must be less than current date", ['entry_date'])]