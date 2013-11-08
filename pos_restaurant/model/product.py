from openerp.osv import fields, osv
from openerp.tools.translate import _


class product_product(osv.Model):
    _inherit = 'product.product'
    _columns = {
        'property_ids': fields.many2many('pos_restaurant.product_property',
                                         'product_property_applied',
                                         'product_id',
                                         'property_id', 'Product Properties',),
    }