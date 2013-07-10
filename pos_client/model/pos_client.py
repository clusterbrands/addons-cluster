from openerp.osv import fields, osv
class pos_client (osv.Model):
    _name = 'pos.client' 
    def create_from_ui(self, cr, uid, customer,context=None):
        self.pool.get('res.partner').create(cr,uid,customer,context=context)
        return True;
        
    def update_from_ui(self, cr, uid, customer,context=None):
        customer_id = customer.pop('id')
        customer.pop('vat');
        self.pool.get('res.partner').write(cr,uid,customer_id,customer,context=context)
        return True;
