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
        http_helper = self.pool.get('pos_fiscal_printer.http_helper')
        request = http_helper.send_request(cr, uid,'get_supported_printers2')     
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
        'tax_rate_ids' : fields.one2many('pos_fiscal_printer.tax_rate',
            'printer_id',string="Tax Rates"),
        'measure_unit_ids' : fields.one2many('pos_fiscal_printer.measure_unit',
            'printer_id',string="Unit of Measure"),
        'header_ids' : fields.one2many('pos_fiscal_printer.invoice_line',
            'printer_id',string="Header",domain=[('type','=','h')]),
        'footer_ids' : fields.one2many('pos_fiscal_printer.invoice_line',
            'printer_id',string="Footers",domain=[('type','=','f')]),
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
    
class tax_rate(osv.Model):

    _name = 'pos_fiscal_printer.tax_rate'
    _columns = {
        'printer_id': fields.many2one('pos_fiscal_printer.printer'),
        'account_tax_id': fields.many2one('account.tax',
            string='Tax',domain=[('type_tax_use','=','sale')]),
        'tax_rate_id': fields.integer(string='Id'),
        'included':fields.boolean(string='Included'),
        'value':fields.float(digits=(12,4),string='Value'),
        'current_value':fields.float(digits=(12,4),string='Current Value'),
    }
    
class measure_unit (osv.Model):
    
    _name = 'pos_fiscal_printer.measure_unit'
    _columns = {
        'printer_id': fields.many2one('pos_fiscal_printer.printer'),
        'product_uom_id': fields.many2one('product.uom',
            string='Tax',domain=[('active','=','True')]),
        'Name':fields.char(size=255,string='Name'),
        'current_code':fields.char(size=255,string='Current Code'),
        'code':fields.char(size=255,string='Code')
    }
    
class invoice_line(osv.Model):
    
    _name = 'pos_fiscal_printer.invoice_line'
    _columns = {
        'printer_id': fields.many2one('pos_fiscal_printer.printer'),
        'type':fields.char(size=1),
        'current_value':fields.char(size=255,string='Current Value'),
        'value':fields.char(size=255,string='Value')
    }
