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
    'name': 'POS Fiscal Printer',
    'category': 'Point of Sale',
    'version': '1.0',
    'author': 'Cluster Brands',
    'website': 'http://www.clusterbrands.com',
    'description': """

This module allows you to use the fiscal printer in the POS interface 

Main features
-------------

* You can print invoices in the POS interface
* Verify that the fiscal printer is configured and connected
* Check the printer status (open top, no paper)
* Verify that the Z report has been generated before opening the POS

Note:
-----
  Only be possible to open the point of sale if this has a 
  fiscal printer configured

""",
    'depends': [
        'pos_client',
        'fiscal_printer',
        'pos_base'
    ],
    'data': [
        'view/point_of_sale_view.xml',
    ],
    'js': [
        'static/src/js/backbone-super-min.js',
        'static/src/js/models.js',
        'static/src/js/widgets.js',
        'static/src/js/devices.js',
        'static/src/js/screens.js',
        'static/src/js/main.js',
    ],
    'css': [
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
