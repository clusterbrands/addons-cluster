from datetime import datetime                                                                       
from dateutil.relativedelta import relativedelta                                                    
from decimal import Decimal                                                                         
import logging                                                                                      
import pdb                                                                                          
import time 

from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _

from osv import osv
from osv import fields

class pos_session(osv.Model):
    _inherit = 'pos.session'

    def create(self, cr, uid, values, context=None):
        context = context or {}
        
        res = super(pos_session, self).create(cr, uid, values, context=context)
        ses_brw = self.browse(cr,uid,res,context=context)

        statement_obj = self.pool.get('account.bank.statement')
       
        config_id = ses_brw.config_id.id

        jobj = self.pool.get('pos.config')

        pos_config = jobj.browse(cr, uid, config_id, context=context)
        bank_statement_ids = []
        for journal in pos_config.journal_ids:
            if journal.payment_instrument_ids:
                for inst in journal.payment_instrument_ids:
                    stmt_id = statement_obj.search(cr, uid, [('pos_session_id','=',res),
                        ('instrument_id','=',False), 
                        ('journal_id','=',journal.id)],
                        context=context)
                    if stmt_id: 
                        #actualizar instrument (inst.id) en el statement 
                        statement_obj.write(cr, uid, [stmt_id[0]], {'instrument_id' : inst.id }, context=context)
                        bank_statement_ids.append(stmt_id[0])
                    else:
                        #crear bank statememt
                        st_number = self.pool.get('ir.sequence').next_by_id(cr, uid,
                                 journal.sequence_id.id, context=context)
                        bank_values = {
                            'journal_id' : journal.id,
                            'instrument_id': inst.id,
                            'user_id' : uid,
                            'state': 'open',
                            'name': st_number,
                            'pos_session_id': res,
                            'company_id' : pos_config.shop_id.company_id.id
                        }
                        statement_id = statement_obj.create(cr, uid, bank_values, context=context)
                        bank_statement_ids.append(statement_id)
            else:
                stmt_id = statement_obj.search(cr, uid, [('pos_session_id','=',res),
                        ('journal_id','=',journal.id)],
                        context=context)
                bank_statement_ids.append(stmt_id[0])
        
        self.pool.get('pos.session').write(cr, uid, res, {'statement_ids':[(6, 0,
            bank_statement_ids)]}, context=context)

        return res 

class pos_order(osv.Model):
    _inherit = 'pos.order'

    def add_payment(self, cr, uid, order_id, data, context=None):
        """Create a new payment for the order"""                                                    
        if not context:                                                                             
            context = {}                                                                            
        statement_line_obj = self.pool.get('account.bank.statement.line')                           
        property_obj = self.pool.get('ir.property')                                                 
        order = self.browse(cr, uid, order_id, context=context)                                     
        args = {                                                                                    
            'amount': data['amount'],                                                               
            'date': data.get('payment_date', time.strftime('%Y-%m-%d')),
            'name': order.name + ': ' + (data.get('payment_name', '') or ''),                       
        }                                                                                           
                                                                                                    
        account_def = property_obj.get(cr, uid, 'property_account_receivable', 'res.partner', context=context)
        args['account_id'] = (order.partner_id and order.partner_id.property_account_receivable \
                             and order.partner_id.property_account_receivable.id) or (account_def and account_def.id) or False
        args['partner_id'] = order.partner_id and order.partner_id.id or None
                                                                                                    
        if not args['account_id']:                                                                  
            if not args['partner_id']:                                                              
                msg = _('There is no receivable account defined to make payment.')                  
            else:                                                                                   
                msg = _('There is no receivable account defined to make payment for the partner: "%s" (id:%d).') % (order.partner_id.name, order.partner_id.id,)
            raise osv.except_osv(_('Configuration Error!'), msg)                                    
                                                                                                    
        context.pop('pos_session_id', False)                                                        
                                                                                                    
        journal_id = data.get('journal', False)                                                     
        statement_id = data.get('statement_id', False)                                              
        assert journal_id or statement_id, "No statement_id or journal_id passed to the method!" 

        args.update({                                                                               
            'statement_id' : statement_id,                                                          
            'pos_statement_id' : order_id,                                                          
            'journal_id' : journal_id,                                                              
            'type' : 'customer',                                                                    
            'ref' : order.session_id.name,                                                          
        })                                                                                          
                                                                                                    
        statement_line_obj.create(cr, uid, args, context=context)                                   
                                                                                                    
        return statement_id
