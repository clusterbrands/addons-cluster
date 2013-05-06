from openerp.osv.orm import except_orm
from openerp.osv import osv, fields
import urllib
import urllib2
import json
import pdb



class printer_brand(osv.Model):    
    _name = 'pos_fiscal_printer.printer_brand'
    _rec_name = 'brand_name'
    _columns = {
        'brand_name': fields.char(size=50)
    }

class printer_model(osv.Model):
    
    _name = 'pos_fiscal_printer.printer_model'
    _rec_name = 'model_name'
    _columns = {
        'model_name': fields.char(size=50),
        'brand_id': fields.many2one('pos_fiscal_printer.printer_brand')        
    }
    
_rec_name = 'partner_id'
class printer(osv.Model):
    _name = 'pos_fiscal_printer.printer'  
   
    def view_init(self,cr, uid, fields_list, context=None):
        context = context or {}  
        http_helper = self.pool.get('pos_fiscal_printer.http_helper')
        try:
            printers = http_helper.send_request(cr, uid,'get_supported_printers2')
        except:
            return ""
        
        pb_obj = self.pool.get('pos_fiscal_printer.printer_brand')
        pm_obj = self.pool.get('pos_fiscal_printer.printer_model')
        for brand in printers:
            brand_id = pb_obj.search(cr,uid,[('brand_name','=',brand)],
                            context=context)
            if not brand_id:
                brand_id = [pb_obj.create(cr,uid,{'brand_name':brand},
                            context)]
            for model in printers[brand]:
                m = pm_obj.search(cr,uid,[('model_name','=',model)],
                        context=context,count=True)
                if (m ==0):
                    pm_obj.create(cr,uid,{'brand_id':brand_id[0],
                        'model_name':model},context)
        
    def read_serial(self, cr, uid, ids, context=None):
        context = context or {}
        print "making something cool"
        pdb.set_trace()
        raise except_orm("Connection Error","Couldn't connect to printer")
        return None
         
    _columns = {
        'name' : fields.char(string='Name', size=50, required=True),
        'brand' : fields.many2one('pos_fiscal_printer.printer_brand',
            string='Brand',required=True),
        'model' : fields.many2one('pos_fiscal_printer.printer_model',
            string='Model',required=True), 
        'port' : fields.char(string='Port', size=100, required=True),
        'type': fields.boolean('Ticket Printer'),
        'serial' : fields.char(string='Serial', size=50),
        'active' : fields.boolean("Active"),
        'payment_method_ids' : fields.one2many('pos_fiscal_printer.payment_method',
            'printer_id',string="Payment Methods"),            
    }
    
class payment_method(osv.Model):
    _name = 'pos_fiscal_printer.payment_method'
    _columns = {
        'printer_id': fields.many2one('pos_fiscal_printer.printer'),   
        'account_journal_id': fields.many2one('account.journal',
            string='Payment Method',domain=[('journal_user','=','True')]),
        'payment_method_id': fields.char(string='Id',size=2),
        'description':fields.char(string='Description', size=50),
        'current_description':fields.char(string='Current Description', size=50),        
    }
    
    _defaults = {
        'current_description': lambda *a: "Not available"
    }
        
