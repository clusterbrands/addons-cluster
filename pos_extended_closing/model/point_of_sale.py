from openerp.osv import osv, fields
class pos_session(osv.Model):
    _inherit = 'pos.session'
    _columns = {
        'statement_ids' : fields.one2many('account.bank.statement', 'pos_session_id', 'Bank Statement'),
    }
