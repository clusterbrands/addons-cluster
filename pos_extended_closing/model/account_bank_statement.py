from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
class account_bank_statement(osv.Model):
    _inherit = "account.bank.statement"
    
    def _compute_difference(self, cr, uid, ids, fieldnames, args, context=None):

        result =  dict.fromkeys(ids, 0.0)

        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = obj.balance_end - obj.balance_cash

        return result
    
    _columns = {
        'balance_cash': fields.float('Cash Balance', digits_compute=dp.get_precision('Account'),
            states={'confirm': [('readonly', True)]}),
        'difference' : fields.function(_compute_difference, method=True, string="Difference", type="float"),
    }
    
