#!/usr/bin/python
# -*- encoding: utf-8 -*-
#############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
###############Credits#######################################################
#    Coded by: Eduardo Ochoa  <eduardo.ochoa@clusterbrands.com.ve>
#                    
#############################################################################
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
{
    'name': "Cluster Brands Purchase Reports",
    'category': "Generic Modules/Purchase",
    'version': "1.0",
    'depends': ['purchase'],
    'author': "Coorporacion ClusterBrands C.A",
    'description': """
    
This module contain a custom purchase
reports used by Cluster Brands C.A

Main features
-------------

    * request_qoutation report with a user signature and venezuelan 
      vat format
    * order report with a user signature and venezuelan vat format

""",
    'data': [
        'purchase_report.xml',
    ],
    'js': [],
    'css': [],
    'qweb': [],
}
