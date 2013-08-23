
# -*- encoding: utf-8 -*-
#
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
# Credits######################################################
#    Coded by: Coorporacion ClusterBrands C.A
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
{
    'name': "POS Base",
    'category': "Generic Modules/Accounting",
    'version': "1.0",
    'depends': ["point_of_sale"],
    'author': "Coorporacion ClusterBrands C.A",
    'description': """

This module contains a set of generic models and views to be used as a 
basis for the development of new modules for the POS

Main features
-------------

""",
    'data': [],
    'js': [
        'static/src/js/backbone-super-min.js',
        'static/src/js/screens.js',
        'static/src/js/main.js',
    ],
    'css': [
        'static/src/css/pos.css',
    ],
    'qweb': [
        'static/src/xml/pos_base.xml',
    ],
}
