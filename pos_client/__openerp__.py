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
    'name': 'POS Client',
    'category': 'Point of Sale',
    'version': '1.0',
    'author': 'Cluster Brands',
    'website': 'http://www.clusterbrands.com',
    'description': """

This module allows you to select and create customers in the POS 
interface.

Main features
-------------

* You can create or update customers in the POS interface
* The customer is directly associated with the order
* The customer information is validated against SENIAT 
* This module can work without connection to the server 

Note:
-----
    You need to specify the country in the post settings to work properly

""",
    'depends': [
        'point_of_sale',
        'pos_base',
        'l10n_ve_fiscal_requirements'
    ],
    'data': [
        'view/point_of_sale_view.xml',
    ],
    'js': [
        'static/src/js/backbone-super-min.js',
        'static/src/js/db.js',
        'static/src/js/models.js',
        'static/src/js/widgets.js',
        'static/src/js/screens.js',
        'static/src/js/main.js',
    ],
    'css': [
        'static/src/css/pos.css',
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
