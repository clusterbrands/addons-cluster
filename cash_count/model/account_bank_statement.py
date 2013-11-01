from openerp.osv import osv, fields
from openerp.tools.translate import _

class account_bank_statement(osv.osv):

    _inherit = 'account.bank.statement' 

    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(account_bank_statement, self).fields_view_get(cr, user, view_id, view_type, context, toolbar, submenu)
        if view_type=='form':
            from lxml import etree
            tree_view = res.get('fields').get('line_ids').get('views').get('tree')
            doc = etree.XML(tree_view.get('arch'))
            for node in doc.xpath("//field[@name='cashier_id']"):
                so = self.pool.get('pos.session')
                session_ids = so.search(cr, user, [('state','<>','closed'), ('user_id','=',user)], context=context)
                if session_ids:
                    session = so.browse(cr, user, session_ids[0], context=context)
                    ids = [cs.cashier_id.id for cs in session.cashier_session_ids]
                    domain = "[('id','in',"+ str(tuple(ids)) + ")]"
                    node.set('domain', domain)
            res['fields']['line_ids']['views']['tree']['arch'] = etree.tostring(doc)                
        return res   

class account_bank_statement_line(osv.Model):
    _inherit = 'account.bank.statement.line'

    def create(self, cr, uid, values, context=None):
        context = context or {}
        obj = self.pool.get('account.bank.statement')
        st = obj.browse(cr, uid, values.get('statement_id'), context=context)
        if st.pos_session_id:
            if st.pos_session_id.cashier_id:
                values.update({'cashier_id':st.pos_session_id.cashier_id.id})
                values.update({'ref':st.pos_session_id.cashier_session_id.name})
        return super(account_bank_statement_line, self).create(cr, uid, values, context=context)

    _columns = {
        'cashier_id': fields.many2one('hr.employee','Cashier'),
    }
