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
{
    'name': 'Payroll Period',
    'category': 'Generic Modules',
    'version': '1.0',
    'author': 'Cluster Brands',
    'website': 'http://www.clusterbrands.com',
    'description': """

Module Description
    
Main features
-------------

Notes:
-----
""",
    'depends': [
        'account',
        'hr_payroll',
        'hr_payroll_account',
    ],
    'data': [
        'view/hr_contract_view.xml',
        'view/hr_payroll_period_view.xml',
        'view/hr_payroll_period_action_menu.xml',
        'wizard/hr_payroll_period_wizard_view.xml',
        'workflow/hr_payroll_period_workflow.xml',
    ],
    'js': [
        'static/src/js/hr_payroll_period.js',
        'static/src/js/backbone-super-min.js',
    ],
    'css': [
        'static/src/css/hr_payroll_period.css',
    ],
    'qweb': [
        'static/src/xml/hr_payroll_period.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
