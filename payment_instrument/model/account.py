from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _


class account_journal(osv.Model):

    '''
    Open ERP Model
    '''

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(
                obj.image,return_medium=False,return_small=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    _inherit = 'account.journal'
    _columns = {
        'image': fields.binary("Image", help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
                                       string="Small-sized image", type="binary", multi="_get_image",
                                       store={
                                       'account.journal': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                                       },
                                       help="Small-sized image of the product. It is automatically "
                                       "resized as a 64x64px image, with aspect ratio preserved. "
                                       "Use this field anywhere a small image is required."),
        'payment_instrument_ids': fields.one2many('payment_instrument.instrument', 'journal_id', 'Payment Instruments'), 
    }
