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

from openerp.osv import osv, fields

class ir_ui_menu(osv.osv):
    _inherit = 'ir.ui.menu'
    _columns = {
                'menu_code': fields.char('Menu Code', size=128)
                }
    
    def get_access_menus(self, cr, uid, ids, parent_menu_id=False, context=None):
        res = []
        menu_ids = self.search(cr, uid, [('parent_id', '=', parent_menu_id)], context=context)
        for menu_obj in self.browse(cr, uid, menu_ids, context=context):
            if menu_obj.action:
                menu_data = {
                             'id': menu_obj.id,
                             'name': menu_obj.name,
                             'action': menu_obj.action.id
                             }
                res.append(menu_data)
            result = self.get_access_menus(cr, uid, ids, menu_obj.id, context=context)
            res.extend(result)
        return res
    
ir_ui_menu()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
