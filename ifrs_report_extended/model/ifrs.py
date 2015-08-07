from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _

class ifrs_ifrs(osv.osv):
    _inherit = 'ifrs.ifrs' 
    #Do not touch _name it must be same as _inherit
    #_name = 'ifrs.ifrs' 

    def _get_period_print_info(self, cr, uid, ids, period_id, report_type, context=None):

        if context is None:
            context = {}
        if report_type == 'all':
            res = _('ALL PERIODS OF THE FISCALYEAR ')
        else:
            period = self.pool.get('account.period').browse(
                cr, uid, period_id, context=context)
            res = str(period.name) + ' [' + str(period.code) + ']'
        return res
