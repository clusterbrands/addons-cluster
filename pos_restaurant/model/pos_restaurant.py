from openerp.osv import fields, osv
from openerp.tools.translate import _


class product_property(osv.Model):
    _name = "pos_restaurant.product_property"

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'single_choice': fields.boolean('Single Choice'),
        'sequence': fields.integer('Sequence Number', required=True),
        'optional_product_ids': fields.many2many('product.product',
                                                 'product_property_rel',
                                                 'property_id',
                                                 'product_id', 'Products',
                                                 domain=[('available_in_pos', '=', True)]),

        'applied_product_ids': fields.many2many('product.product',
                                                'product_property_applied',
                                                'property_id',
                                                'product_id', 'Applied Products',
                                                domain=[('available_in_pos', '=', True)]),
    }

    _order = 'sequence'
