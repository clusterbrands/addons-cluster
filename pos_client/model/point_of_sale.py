from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import logging
import pdb
import time

import openerp
from openerp import netsvc, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product

class pos_config (osv.Model):
    _inherit = 'pos.config' 
    _columns = {
        'country_id': fields.many2one('res.country',string="Country",required=True),
    }
class pos_order(osv.osv):
    _inherit = "pos.order"
    
    def create_from_ui(self, cr, uid, orders, context=None):
        obj = self.pool.get("res.partner");
        for tmp_order in orders:
            order = tmp_order['data']      
            vat = order.get("partner_vat")
            partner_id = obj.search(cr,uid,[("vat","=",vat)],context=context)
            if (partner_id):
                order_id = super(pos_order,self).create_from_ui(cr, uid, orders, context=context)
                self.write(cr,uid,order_id,{"partner_id":partner_id[0]},context=context)
            else:
                raise osv.except_osv(_('Failed to create order!'), _('Not partner found!'))
            
        return True
        
