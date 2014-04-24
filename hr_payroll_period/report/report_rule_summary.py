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
import time
from openerp.report import report_sxw


class report_rule_sumary(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_rule_sumary, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_details_by_rule_category': self.get_details_by_rule_category,
            'get_formatted_vat': self.get_formatted_vat,
        })

    def get_formatted_vat(self, company):
        vat = company.partner_id.vat
        if company.country_id.code == "VE":
            return vat[2]+"-"+vat[3:10]+"-"+vat[11]
        return vat

    def get_details_by_rule_category(self, obj):
        payslip_line = self.pool.get('hr.payslip.line')
        rule_cate_obj = self.pool.get('hr.salary.rule.category')
        rule_obj = self.pool.get('hr.salary.rule')

        def get_recursive_parent(rule_categories):
            if not rule_categories:
                return []
            if rule_categories[0].parent_id:
                rule_categories.insert(0, rule_categories[0].parent_id)
                get_recursive_parent(rule_categories)
            return rule_categories

        res = []
        result = {}
        ids = []

        for id in range(len(obj)):
            ids.extend([s.id for s in obj[id].details_by_salary_rule_category])
        if ids:
            self.cr.execute('''SELECT pl.salary_rule_id, pl.category_id, sum(pl.total) as total FROM hr_payslip_line as pl \
                LEFT JOIN hr_salary_rule_category AS rc on (pl.category_id = rc.id) \
                WHERE pl.id in %s \
                GROUP BY rc.parent_id, pl.sequence, pl.category_id, pl.salary_rule_id \
                ORDER BY pl.sequence, rc.parent_id''',(tuple(ids),))
            
            for x in self.cr.fetchall():
                result.setdefault(x[1], [])
                result[x[1]].append((x[0],x[2]))
            for key, values in result.iteritems():
                rule_categories = rule_cate_obj.browse(self.cr, self.uid, [key])
                parents = get_recursive_parent(rule_categories)
                category_total = 0
                for line in values:
                    category_total += line[1]
                level = 0
                for parent in parents:
                    res.append({
                        'rule_category': parent.name,
                        'name': parent.name,
                        'code': parent.code,
                        'level': level,
                        'total': category_total,
                    })
                    level += 1
                for line in values:
                    brw = rule_obj.browse(self.cr, self.uid, line[0])
                    res.append({
                        'rule_category': brw.name,
                        'name': brw.name,
                        'code': brw.code,
                        'total': line[1],
                        'level': level
                    })
        return res


report_sxw.report_sxw('report.rule.summary', 'hr.payslip',
                      'addons/hr_payroll_period/report/report_rule_summary.mako', parser=report_rule_sumary)
