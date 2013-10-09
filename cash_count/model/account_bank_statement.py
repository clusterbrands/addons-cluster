from openerp.osv import osv, fields
from openerp.tools.translate import _


class account_bank_statement_line(osv.Model):
    _inherit = 'account.bank.statement.line'

    _columns = {
        'cashier_id': fields.many2one('hr.employee', 'Cashier',
                                      domain=[('active', '=', True),
                                              ('cashier', '=', True)])
    }
