
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _

from osv import osv
from osv import fields

class pos_session(osv.Model):
    _inherit = 'pos.session'

    def create(self, cr, uid, values, context=None):
        context = context or {}
        config_id = values.get('config_id', False) or context.get('default_config_id', False)
        if not config_id:
            raise osv.except_osv( _('Error!'),
                _("You should assign a Point of Sale to your session."))
                                                                                                    
        # journal_id is not required on the pos_config because it does not                          
        # exists at the installation. If nothing is configured at the                               
        # installation we do the minimal configuration. Impossible to do in                         
        # the .xml files as the CoA is not yet installed.                                           
        jobj = self.pool.get('pos.config')
        pos_config = jobj.browse(cr, uid, config_id, context=context)
        context.update({'company_id': pos_config.shop_id.company_id.id})
        if not pos_config.journal_id:
            jid = jobj.default_get(cr, uid, ['journal_id'], context=context)['journal_id']
            if jid:
                jobj.write(cr, uid, [pos_config.id], {'journal_id': jid}, context=context)          
            else:
                raise osv.except_osv( _('error!'),                                                  
                    _("Unable to open the session. You have to assign a sale journal to your point of sale."))
                                                                                                    
        # define some cash journal if no payment method exists                                      
        if not pos_config.journal_ids:
            journal_proxy = self.pool.get('account.journal')
            cashids = journal_proxy.search(cr, uid, [('journal_user', '=', True), ('type','=','cash')], context=context)
            if not cashids:
                cashids = journal_proxy.search(cr, uid, [('type', '=', 'cash')], context=context)   
                if not cashids:
                    cashids = journal_proxy.search(cr, uid, [('journal_user','=',True)], context=context)
                                                                                                    
            jobj.write(cr, uid, [pos_config.id], {'journal_ids': [(6,0, cashids)]})
                                                                                                    
                                                                                                    
        pos_config = jobj.browse(cr, uid, config_id, context=context)
        bank_statement_ids = []
        for journal in pos_config.journal_ids:
            bank_values = {
                'journal_id' : journal.id,
                'user_id' : uid,
                'company_id' : pos_config.shop_id.company_id.id
            }
            statement_id = self.pool.get('account.bank.statement').create(cr, uid, bank_values, context=context)
            bank_statement_ids.append(statement_id)
                                                                                                    
        values.update({
            'name' : pos_config.sequence_id._next(),
            'statement_ids' : [(6, 0, bank_statement_ids)],
            'config_id': config_id 
        })                                                                                          
                                                                                                    
        return super(pos_session, self).create(cr, uid, values, context=context)
