from openerp.osv import osv, fields
from openerp.tools.translate import _

class cashier(osv.Model):
    _name = "cash.count.cashier"
    
    _columns = {
        "name":fields.char(string="Name", size=50, required=True),
        "password":fields.char(string="Password", size=50, 
                               required=True),
        
    }