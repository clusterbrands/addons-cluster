from openerp.osv import osv, fields
class pos_config (osv.Model):
    _inherit = 'pos.config' 
    _columns = {
        'printer_id': fields.many2one('pos_fiscal_printer.printer',string="Fiscal Printer"),
    }

