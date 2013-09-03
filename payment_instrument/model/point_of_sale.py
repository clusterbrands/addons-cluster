
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
