# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################

{
    'name' : "POS Cashier",
    'category' : "Test",
    'version' : "1.0",
    'depends' : ["point_of_sale"],
    'author' : "Me",
    'description': """
    
This module allows you to use cashier's in the POS interface without 
them be OpenERP users.
                                                                                
""",
    'data' : [
        'view/pos_cashier_view.xml',
        'view/pos_cashier_action_menu.xml',
        'view/point_of_sale_view.xml',
        'wizard/pos_cashier_session_opening.xml',
        'wizard/pos_session_opening.xml',
    ], 
    
}
