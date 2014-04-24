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
from openerp.report import report_sxw


class report_payroll_sumary(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_payroll_sumary, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_allocation_total': self.get_allocation_total,
            'get_deduction_total': self.get_deduction_total,
            'get_total_net': self.get_total_net,
            'get_formatted_vat': self.get_formatted_vat,
        })

    def get_formatted_vat(self, company):
        vat = company.partner_id.vat
        if company.country_id.code == "VE":
            return vat[2]+"-"+vat[3:10]+"-"+vat[11]
        return vat

    def get_allocation_total(self, obj):
        payslip_line = self.pool.get('hr.payslip.line')
        amount = 0
        for id in range(len(obj)):
            if obj[id].appears_on_payslip == True:
                if obj[id].total > 0:              
                    amount += obj[id].total
        return amount

    def get_deduction_total(self, obj):
        payslip_line = self.pool.get('hr.payslip.line')
        amount = 0
        for id in range(len(obj)):
            if obj[id].appears_on_payslip == True:
                if obj[id].total < 0:              
                    amount += obj[id].total
        return amount 

    def get_total_net(self, obj):
        alw = self.get_allocation_total(obj)
        dud = self.get_deduction_total(obj)
        return alw + dud 

report_sxw.report_sxw('report.payroll.summary', 'hr.payslip',
                      'addons/hr_payroll_period/report/report_payroll_summary.mako', parser=report_payroll_sumary)