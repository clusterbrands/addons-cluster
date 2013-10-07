#!/usr/bin/python                                                               
# -*- encoding: utf-8 -*-                                                       
############################################################################### 
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) Vauxoo (<http://vauxoo.com>).
#    All Rights Reserved                                                        
################# Credits###################################################### 
#    Coded by: Luis Escobar <luis@vauxoo.com>
#    Audited by: Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################### 
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
###############################################################################    

from openerp.osv import fields, osv
from openerp.tools.translate import _

class close_lot(osv.TransientModel):

    '''Close Lot Wizard'''

    _name = 'close.lot'
    _columns = {
        'nro_lot':fields.char('Number of Lot', 25, help='Number Identification of Bank Lot',
            required=True), 
        'note': fields.text('Note', translate=True),
    }

    def exec_lot(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        cls_lt = self.browse(cr, uid, ids, context=context)[0]
        rule_obj = self.pool.get('payment_instrument.rule') 
        stmt_brw = self.pool.get(context.get('active_model')).browse(cr, uid,
                context.get('active_id'), context=context)
        inst = stmt_brw.instrument_id
        amount_total = stmt_brw.balance_end
        journal = stmt_brw.journal_id 
        amount = 0.0 
        amount_perc = 0.0
        move_id = self.pool.get('account.move').create(cr, uid, {
            'ref' : cls_lt.nro_lot,
            'journal_id': journal.id,
        }, context=context) 
        move_lines = []
        rule_ids = rule_obj.search(cr, uid,
                [('instrument_id','=',inst.id),('amount_select','=','percentage')], context=context)
        for rule in rule_obj.browse(cr, uid, rule_ids,
                context=context):
            amount = amount_total * (rule.amount_percentage/100)
            amount_perc+= amount
            line = {
                    'name': rule.name,
                    'account_id': rule.condition_account_id.id,
                    'credit': 0.0,
                    'debit': amount, 
                    'partner_id': False,
                }
            move_lines.append(line)

        amount = amount_total - amount_perc 
        line = {
                    'name': 'Bank Account',
                    'account_id': journal.bank_account.id,
                    'credit': 0.0,
                    'debit': amount, 
                    'partner_id': False,
                }
        move_lines.append(line)

        line = {
                'name': journal.name, 
                'account_id': journal.default_credit_account_id.id,
                'credit': amount_total, 
                'debit': 0.0,
                'partner_id': False,
            }
        move_lines.append(line)

        all_lines = []

        for l in move_lines:
             all_lines.append((0, 0,l))

        self.pool.get("account.move").write(cr, uid, [move_id], {'line_id':all_lines},
                context=context)

        self.pool.get('account.bank.statement').write(cr, uid, [context.get('active_id')],{
                'process_lot': 'processed',
                'lot_note': cls_lt.note,
            }, context=context)

        obj_model = self.pool.get('ir.model.data')                                                     
        model_data_ids = obj_model.search(                                                             
            cr, uid, [('model', '=', 'ir.ui.view'),                                                    
                     ('name', '=', 'view_move_form')])                                                
        resource_id = obj_model.read(cr, uid, model_data_ids,                                          
                                    fields=['res_id'])[0]['res_id']                                    
        return {                                                                                       
           'view_type': 'form',
           'view_mode': 'form',
           'res_model': 'account.move',
           'views': [(resource_id, 'form')],
           'res_id': move_id,
           'type': 'ir.actions.act_window',
           'context': {},
        }
