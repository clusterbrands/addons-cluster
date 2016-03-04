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

from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _get_move_lines(self, cr, uid, ids, to_wh, period_id, pay_journal_id,
                        writeoff_acc_id, writeoff_period_id,
                        writeoff_journal_id, date, name, context=None):

    	context = context or {}
        rp_obj = self.pool.get('res.partner')
        ids = isinstance(ids, (int, long)) and [ids] or ids
        res = super(account_invoice, self)._get_move_lines(
            cr, uid, ids, to_wh, period_id, pay_journal_id, writeoff_acc_id,
            writeoff_period_id, writeoff_journal_id, date, name,
            context=context)
        
        acc_obj = self.pool.get('account.account')
        for line in res:
        	acc_id = line[2].get('account_id')
        	acc_brw = acc_obj.browse(cr, uid, acc_id, context)
        	if acc_brw.partner_id:
        		line[2].update({'partner_id': acc_brw.partner_id.id})
        return res        	
