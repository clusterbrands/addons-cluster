from openerp.osv.orm import except_orm,BaseModel
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
   
    def read_payment_methods(self, cr, uid, ids, context=None):
        context = context or {}    
        http_helper = self.pool.get('pos_fiscal_printer.http_helper')
        response = http_helper.send_command(cr, uid,ids,'read_payment_methods')
        
    def read_tax_rates(self, cr, uid, ids, context=None):
        context = context or {}
        tax_rates = {}   
        http_helper = self.pool.get('pos_fiscal_printer.http_helper')
        response = http_helper.send_command(cr, uid,ids,'read_tax_rates')        
        tax_rates = response.get('tax_rates')
        obj = self.pool.get('pos_fiscal_printer.tax_rate')
        for tr in tax_rates:
            tax_id = obj.search(cr,uid,[('code','=',tr.get('code'))],
                        context=context)
            if not tax_id:
                vals = {'printer_id': ids[0],
                       'current_value':tr.get('value'),
                       'value':tr.get('value'),
                       'description':tr.get('description'),
                       'code':tr.get('code')
                    }
                obj.create(cr,uid,vals,context=context)
            else:
                obj.write(cr,uid,tax_id,{'current_value':tr.get('value')},
                context=context)
        return True
        
    def write_tax_rates(self, cr, uid, ids, context=None):
        context = context or {}
        tax_rates = []
        printer = self.browse(cr,uid,ids)[0]
        for tax in printer.tax_rate_ids:
            tax_rates.append({'code':tax.code,'value':tax.value})
        
        params = {'tax_rates':tax_rates}
        http_helper = self.pool.get('pos_fiscal_printer.http_helper')
        response = http_helper.send_command(cr, uid,ids,'write_tax_rates',params)   
        
        #~ tax_rate = self.pool.get('pos_fiscal_printer.tax_rate')
        #~ for tax in printer.tax_rate_ids:
            #~ tax_rate.write(cr,uid,tax.id,{'value':tax.current_value},
                      #~ context=context)
        
    def read_serial(self, cr, uid, ids, context=None):
        context = context or {}    
        http_helper = self.pool.get('pos_fiscal_printer.http_helper')
        response = http_helper.send_command(cr, uid,ids,'read_printer_serial')   
        serial = response.get('serial')  
        self.write(cr,uid,ids,{'serial':serial},context=context)
        return True
        
    def view_init(self,cr, uid, fields_list, context=None):
        context = context or {}  
        http_helper = self.pool.get('pos_fiscal_printer.http_helper')       
        try:
            response = http_helper.send_command(cr, uid,[],'get_supported_printers')
            printers = response
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
        return True
         
    _columns = {
        'name' : fields.char(string='Name', size=50, required=True),
        'brand' : fields.many2one('pos_fiscal_printer.printer_brand',
            string='Brand',required=True),
        'model' : fields.many2one('pos_fiscal_printer.printer_model',
            string='Model',required=True), 
        'port' : fields.char(string='Port', size=100, required=True),
        'type': fields.boolean('Ticket Printer'),
        'serial' : fields.char(string='Serial', size=50),
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
        'code': fields.char(string='Tax Code',size=4),
        'description':fields.char(string='Description',size=255),
        'value':fields.float(digits=(12,2),string='Value'),
        'current_value':fields.float(digits=(12,2),string='Current Value'),
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
