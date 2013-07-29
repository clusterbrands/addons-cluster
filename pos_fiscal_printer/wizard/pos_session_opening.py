from openerp.osv import osv, fields
from openerp.tools.translate import _


class pos_session_opening(osv.osv_memory):
    _inherit = 'pos.session.opening'

    def open_ui(self, cr, uid, ids, context=None):
        context = context or {}
        obj = self.pool.get("fiscal_printer.printer")
        printer = obj.get_printer(cr, uid, context=context)
        res = printer.send_command("has_pending_reduce")
        if res.get("reduce"):
            raise osv.except_osv("Error", _("Has pending to do a z report"))
        else:
            printer = obj.get_assigned_printer(cr, uid, context=context)
            printer.send_command(cr, uid, ids, 'has_pending_reduce')
            return super(self, pos_session_opening).open_ui(cr, uid, ids, context=context)
