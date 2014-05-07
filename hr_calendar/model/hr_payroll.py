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

from openerp.osv import osv, fields
from openerp.tools.translate import _


class hr_payslip(osv.Model):

    _inherit = "hr.payslip"

    def get_utils_dict(self, cr, uid, payslip_id, context=None):
        context = context or {}
        calendars = {}
        obj_calendar = self.pool.get('hr.calendar')
        obj_payslip = self.pool.get('hr.payslip')
        payslip = obj_payslip.browse(cr, uid, payslip_id, context=context)
        c_ids = obj_calendar.search(cr, uid, [], context=context)
        for c in obj_calendar.browse(cr, uid, c_ids, context=context):
            calendars[c.code] = c.count_dates(
                payslip.date_from, payslip.date_to)
        utils = super(hr_payslip, self).get_utils_dict(
            cr, uid, payslip_id, context=context)
        utils.update({'calendars': calendars})
        return utils
