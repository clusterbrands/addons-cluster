from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
import re


class account_bank_statement(osv.Model):

    _inherit = "account.bank.statement"

    def _count_transactions(self, cr, uid, ids, fieldnames, args, context=None):
        """
        Compute the number of transactions for each bank.statement, 
        ignoring the return transactions
        """
        result = dict.fromkeys(ids, 0)
        for st in self.browse(cr, uid, ids, context=context):
            for line in st.line_ids:
                if not re.match("(.*) return", line.name):
                    result[st.id] += 1
        return result

    _columns = {
        'transactions_count': fields.function(_count_transactions, method=True, string="Transactions Count", type="integer")
    }
