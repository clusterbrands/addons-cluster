from openerp.osv import osv, fields
from openerp.tools.translate import _

class account_bank_statement(osv.osv):

    _inherit = 'account.bank.statement' 

    def _compute_difference(self, cr, uid, ids, fieldnames, args, context=None):
        result =  dict.fromkeys(ids, 0.0)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = obj.balance_end_x - obj.balance_end
        return result

    def _get_statement2(self, cr, uid, ids, context=None):
        context = context or {}
        res = []
        obj = self.pool.get('cash.count.reportx.line')
        for line in obj.browse(cr, uid, ids, context=context):
            res.append(line.statement_id.id)
        return res


    def _balance_end_x(self, cr, uid, ids, name, attr, context=None):
        context = context or {}
        res = {}
        for statement in self.browse(cr, uid, ids, context=context):
            res[statement.id] = statement.balance_start
            for line in statement.reportx_line_ids:
                res[statement.id] += line.end_balance
        return res

    _columns = {
        'difference' : fields.function(_compute_difference, method=True, string="Difference", type="float"),
        'reportx_line_ids': fields.one2many('cash.count.reportx.line',
                                            'statement_id',
                                            'Report X Lines'),
        'balance_end_x': fields.function(_balance_end_x, 
            store={
                'cash.count.reportx.line': (_get_statement2,['end_balance'],10),
            },
            string="Cashiers Balance"), 
    }

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
