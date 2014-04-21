# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2013 Serpent Consulting Services (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################
from openerp.osv import osv
from openerp.tools.translate import _
from openerp.report import report_sxw
from openerp.tools import amount_to_text_en

class payslip_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(payslip_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_payslip_lines': self.get_payslip_lines,
            'get_allocation_total': self.get_allocation_total,
            'get_deduction_total': self.get_deduction_total,
            'get_total_net': self.get_total_net,
        })

    def get_payslip_lines(self, obj):
        payslip_line = self.pool.get('hr.payslip.line')
        res = []
        ids = []
        for id in range(len(obj)):
            if obj[id].appears_on_payslip == True:
                ids.append(obj[id].id)
        if ids:
            res = payslip_line.browse(self.cr, self.uid, ids)
        return res

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

report_sxw.report_sxw('report.payslip.webkit', 'hr.payslip', 'addons/hr_payroll_period/report/report_payslip_webkit.mako', parser=payslip_report)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: