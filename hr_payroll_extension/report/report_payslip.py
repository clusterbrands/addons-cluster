#-*- coding:utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.report import report_sxw
from openerp.addons.hr_payroll.report import report_payslip


class payslip_report_cluster(report_payslip.payslip_report):

    def __init__(self, cr, uid, name, context):
        super(payslip_report_cluster, self).__init__(cr, uid, name, context)
    	self.localcontext.update({
            'get_allocation_total': self.get_allocation_total,
            'get_deduction_total': self.get_deduction_total,
            'get_total_net': self.get_total_net,
        }) 
        
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

class wrapped_report_payslip_cluster(osv.AbstractModel):
    _name = 'report.hr_payroll_extension.report_payslip'
    _inherit = 'report.abstract_report'
    _template = 'hr_payroll_extension.report_payslip'
    _wrapped_report_class = payslip_report_cluster