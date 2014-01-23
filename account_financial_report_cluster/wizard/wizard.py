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

from osv import osv, fields
from tools.translate import _


class wizard_report(osv.osv_memory):
    _inherit = 'wizard.report'

    _columns = {
        'hide_views': fields.boolean("Hide 'View' Accounts", help="Hide Accounts types 'View'"),
        'partial_sumarize': fields.boolean("Partial Summarize?", help="help='Checking will add a new line at the end of each account which will Summarize Columns in Report'"),
    }
    
    def onchange_afr_id(self, cr, uid, ids, afr_id, context=None):
         context = context or {}
         res =  super(wizard_report, self).onchange_afr_id(cr, uid, ids, afr_id, context)
         if not afr_id:
            return res
         afr_brw = self.pool.get('afr').browse(cr, uid, afr_id, context=context)         
         res['value'].update({'hide_views': afr_brw.hide_views or False})
         res['value'].update({'partial_sumarize': afr_brw.partial_sumarize or False})
         return res
