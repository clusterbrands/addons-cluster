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
#++++++++++++++++++++++++++++++++++++++++++++++++se++++++++++++++++++++++++++++++

import datetime
from openerp.osv import osv, fields
from openerp.tools.translate import _


class hr_calendar (osv.Model):
    _name = "hr.calendar"

    def count_dates(self, cr, uid, ids, from_date, to_date, context=None):
        context = context or {}
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        obj = self.browse(cr, uid, ids, context=context)[0]
        count = 0.0
        for date in eval(obj.dates):
            dt = datetime.datetime.strptime(date, '%m/%d/%Y').date()
            if (dt >= from_date) and (dt <= to_date):
                count += 1;
        return count  

    _columns = {
        'name': fields.char('Name', size=255, required=True),
        'code': fields.char('Code', size=64, required=True),
        'limit': fields.selection([
                                   ('end_of_period', 'End of Period'),
                                   # ('end_of_year', 'End of Year'),
                                   # ('holidays_end_date', 'Holiday Return Date'),
                                   # ('previous_period', 'Previous Period'),
                                   # ('liquidation_date', 'Liquidation Date'),
                                   # ('previous_month', 'Previous Month')
                                  ],'Limit', select=True),
        'dates': fields.text('Dates'), 
    }

    _defaults = {  
        'limit': 'end_of_period',  
        }


