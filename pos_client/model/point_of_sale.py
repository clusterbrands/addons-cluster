from openerp.osv import fields, osv
class pos_config (osv.Model):
    _inherit = 'pos.config' 
    _columns = {
        'country_id': fields.many2one('res.country',string="Country"),
    }
