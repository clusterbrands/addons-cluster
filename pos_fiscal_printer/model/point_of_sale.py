#!/usr/bin/python
# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Eduardo Ochoa    <eduardo.ochoa@clusterbrands.com.ve>
#                               <elos3000@gmail.com>
#############################################################################
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
################################################################################

from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import logging
import pdb
import time

import openerp
from openerp import netsvc, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product
  
class pos_order (osv.Model):
    
    _inherit = 'pos.order' 
        
    def create_from_ui(self, cr, uid, orders, context=None):
        obj = self.pool.get("res.partner");
        for tmp_order in orders:
            order = tmp_order['data']      
            order_id = super(pos_order,self).create_from_ui(cr, uid, orders, context=context)
            self.write(cr,uid,order_id,
                       {"invoice_printer":order['invoice_printer'],
                       "fiscal_printer":order['fiscal_printer']},
                       context=context)
        return True
                
    def action_invoice(self, cr, uid, ids, context=None):
        wf_service = netsvc.LocalService("workflow")
        inv_ref = self.pool.get('account.invoice')
        inv_line_ref = self.pool.get('account.invoice.line')
        product_obj = self.pool.get('product.product')
        inv_ids = []

        for order in self.pool.get('pos.order').browse(cr, uid, ids, context=context):
            if order.invoice_id:
                inv_ids.append(order.invoice_id.id)
                continue

            if not order.partner_id:
                raise osv.except_osv(_('Error!'), _('Please provide a partner for the sale.'))

            acc = order.partner_id.property_account_receivable.id
            inv = {
                'name': order.name,
                'origin': order.name,
                'account_id': acc,
                'journal_id': order.sale_journal.id or None,
                'type': 'out_invoice',
                'reference': order.name,
                'partner_id': order.partner_id.id,
                'comment': order.note or '',
                'currency_id': order.pricelist_id.currency_id.id, # considering partner's sale pricelist's currency
                'invoice_printer':order.invoice_printer,
                'fiscal_printer':order.fiscal_printer,
            }
            inv.update(inv_ref.onchange_partner_id(cr, uid, [], 'out_invoice', order.partner_id.id)['value'])
            if not inv.get('account_id', None):
                inv['account_id'] = acc
            inv_id = inv_ref.create(cr, uid, inv, context=context)

            self.write(cr, uid, [order.id], {'invoice_id': inv_id, 'state': 'invoiced'}, context=context)
            inv_ids.append(inv_id)
            for line in order.lines:
                inv_line = {
                    'invoice_id': inv_id,
                    'product_id': line.product_id.id,
                    'quantity': line.qty,
                }
                inv_name = product_obj.name_get(cr, uid, [line.product_id.id], context=context)[0][1]
                inv_line.update(inv_line_ref.product_id_change(cr, uid, [],
                                                               line.product_id.id,
                                                               line.product_id.uom_id.id,
                                                               line.qty, partner_id = order.partner_id.id,
                                                               fposition_id=order.partner_id.property_account_position.id)['value'])
                if line.product_id.description_sale:
                    inv_line['note'] = line.product_id.description_sale
                inv_line['price_unit'] = line.price_unit
                inv_line['discount'] = line.discount
                inv_line['name'] = inv_name
                inv_line['invoice_line_tax_id'] = [(6, 0, [x.id for x in line.product_id.taxes_id] )]
                inv_line_ref.create(cr, uid, inv_line, context=context)
            inv_ref.button_reset_taxes(cr, uid, [inv_id], context=context)
            wf_service.trg_validate(uid, 'pos.order', order.id, 'invoice', cr)

        if not inv_ids: return {}

        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
        res_id = res and res[1] or False
        return {
            'name': _('Customer Invoice'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': 'account.invoice',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': inv_ids and inv_ids[0] or False,
        } 

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        """Remove the fields invoice_printer and fiscal_priter for 
        the view if _get_loc_req is True
        """
        context = context or {}
        res = super(pos_order,self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        if view_type == 'tree':          
            if  self._get_loc_req(cr,uid,context=context):
                for node in doc.xpath("//field[@name='invoice_printer']"):
                    doc.remove(node)
                for node in doc.xpath("//field[@name='fiscal_printer']"):
                    doc.remove(node)
            res['arch'] = etree.tostring(doc)
        return res
    
    def _get_loc_req(self, cr, uid, context=None):
        """Get if a field is required or not by a Localization
        @param uid: Integer value of the user
        """
        context = context or {}
        res = True
        ru_brw = self.pool.get('res.users').browse(cr,uid,uid,context=context)
        rc_obj = self.pool.get('res.company')
        rc_brw = rc_obj.browse(cr, uid, ru_brw.company_id.id, context=context)
        
        if rc_brw.country_id and rc_brw.country_id.code == 'VE' and rc_brw.printer_fiscal:
            res = False
        return res
    
    _columns = {
        'invoice_printer' : fields.char('Fiscal Printer Invoice Number', size=64, required=False,help="Fiscal printer invoice number, is the number of the invoice on the fiscal printer"),
        'fiscal_printer' : fields.char('Fiscal Printer Number', size=64, required=False,help="Fiscal printer number, generally is the id number of the printer."),
        'loc_req':fields.boolean('Required by Localization', help='This fields is for technical use'),
    }
    _defaults ={
        'loc_req': _get_loc_req
    }
