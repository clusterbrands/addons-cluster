# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
#

{
    'name': "POS Client",
    'category': "Test",
    'version': "1.0",
    'depends': ['point_of_sale','pos_base','l10n_ve_fiscal_requirements'],
    'author': "Me",
    'description': """Enables add clients in the POS module orders""",
    'init_xml': [
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
    'qweb': ['static/src/xml/pos.xml'],
}
