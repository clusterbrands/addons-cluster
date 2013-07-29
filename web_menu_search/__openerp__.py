# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 ZestyBeanz Technologies Pvt. Ltd.
#    (http://wwww.zbeanztech.com)
#    contact@zbeanztech.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'OpenERP Menu Search',
    'version': '1.0',
    'category': 'Menu Search',
    'sequence': 1,
    'summary': 'OpenERP Menu Search',
    'description': """Module to search menu in OpenERP""",
    'author': 'Zesty Beanz Technologies',
    'website': 'http://www.zbeanztech.com',
    'images': [],
    'depends': ['web'],
    'data': [
             'ir_ui_menu_view.xml'
             ],
    'demo': [],
    'test': [],
    'js': [
           'static/src/js/menu_search.js',
           'static/src/js/url_security.js'
           ],
    'qweb': [
             'static/src/xml/menu_search.xml'
             ],
    'css' : [
             "static/src/css/menu_search.css"
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
