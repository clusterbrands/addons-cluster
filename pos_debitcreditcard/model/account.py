#!/usr/bin/python
# -*- encoding: utf-8 -*-                                                          
############################################################################### 
#    Module Writen to OpenERP, Open Source Management Solution                  
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).                 
#    All Rights Reserved                                                        
################# Credits###################################################### 
#    Coded by: Luis Escobar <luis@vauxoo.com>                                      
#    Audited by:  Humberto Arocha <humbertoarocha@gmail.com>                    
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

import openerp                                                                     
from openerp import netsvc, tools                                                  
from openerp.osv import fields, osv                                                
from openerp.tools.translate import _

class account_journal(osv.Model):
    _inherit = 'account.journal'
    _columns = {
        'bank_account':fields.many2one('account.account', """Bank Account""", help="""Bank Account
            to imputing computation of instrument rules"""),
    }

class account_bank_statement(osv.Model):
    _inherit = 'account.bank.statement'
    _columns = {
        'lot_note': fields.text('Lot Note', translate=True), 
        'process_lot':fields.selection([('none','No Processed'),
                                        ('processed','Processed')],'Lot Status',
                                        help="""Indicate if was process the lot"""), 
    }
    _defaults = {
            'process_lot': 'none',
    }
