from openerp.osv import osv, fields
from openerp.tools.translate import _


class pos_session_opening(osv.osv_memory):
    _inherit = 'pos.session.opening'

    def open_ui(self, cr, uid, ids, context=None):
        context = context or {}
        
        obj = self.pool.get("fiscal_printer.printer")
        printer = obj.get_printer(cr, uid, context=context)
        
        res = printer.send_command("check_printer_status")
        if res.get("status") == "error":
            raise osv.except_osv("Error", _(res.get('error')))

        res = printer.send_command("has_pending_reduce")
        if res.get("reduce"):
            raise osv.except_osv("Error", _("Has pending to do a z report"))
        else:
            return super(pos_session_opening, self).open_ui(cr, uid, ids, context=context)
