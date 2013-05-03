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
        url = "http://localhost:8069/pos/get_supported_printers"            
        req = urllib2.Request(url)
        try:
            res = urllib2.urlopen(req)                      
        except:
            print "Not found 404"
            
        printers = json.loads(res.read())
        pb_obj = self.pool.get('pos_fiscal_printer.printer_brand')
        pm_obj = self.pool.get('pos_fiscal_printer.printer_model')
        for brand in printers:
            brand_id = pb_obj.search(cr,uid,[('brand_name','=',brand)],context=context)
            if not brand_id:
                brand_id = [pb_obj.create(cr,uid,{'brand_name':brand},context)]
            for model in printers[brand]:
                m = pm_obj.search(cr,uid,[('model_name','=',model)],
                        context=context,count=True)
                if (m ==0):
                    pm_obj.create(cr,uid,{'brand_id':brand_id[0],'model_name':model},context)
            
    
    def _get_brands(self,cursor,user_id,context=None):
                
        url = "http://localhost:8069/pos/get_supported_brands"    
        req = urllib2.Request(url)
        try:
            res = urllib2.urlopen(req)
        except:
            print "Not found 404"
        brands = json.loads(res.read())
        return [(brand,brand) for brand in brands]
        
         
    _columns = {
        'name' : fields.char(string='Name', size=50, required=True),
        'brand' : fields.many2one('pos_fiscal_printer.printer_brand',
            string='Brand',required=True),
        'model' : fields.many2one('pos_fiscal_printer.printer_model',
            string='Model',required=True), 
        'port' : fields.char(string='Port', size=100, required=True),
        'type': fields.boolean('Ticket Printer'),
        'serial' : fields.char(string='Serial', size=50, required=True),
        'active' : fields.boolean("Active"),            
    }
