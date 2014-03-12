from openerp import netsvc
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class wizard_reportx(osv.osv_memory):
    _name = "wizard.reportx"

    _columns = {
        'pos_session_id': fields.many2one('pos.session', 'PoS Session'),
        'cashier_session_id': fields.many2one('cash.count.cashier.session', 'Cashier Session'),
        'user_id': fields.many2one('res.users', 'Responsible', readonly=True),
        'cashier_id': fields.many2one('hr.employee', 'Cashier', readonly=True),
        'config_id': fields.many2one('pos.config', 'Point of Sale',
                                     readonly=True),
        'line_ids': fields.one2many('wizard.reportx.line', 'reportx_id',
                                    'Payment Methods', required=False),
    }

    def default_get(self, cr, uid, fieldnames, context=None):
        context = context or {}
        sop_obj = self.pool.get('pos.session.opening')
        sop = sop_obj.browse(
            cr, uid, context.get('active_id'), context=context)
        result = {}
        result['pos_session_id'] = sop.pos_session_id.id
        result[
            'cashier_session_id'] = sop.pos_session_id.cashier_session_id.id
        result['user_id'] = sop.pos_session_id.user_id.id
        result['cashier_id'] = sop.pos_session_id.cashier_id.id
        result['config_id'] = sop.pos_session_id.config_id.id
        return result

    def end_session(self, cr, uid, ids, context=None):
        context = context or {}
       
        obj = self.pool.get("fiscal_printer.printer")
        printer = obj.get_printer(cr, uid, context=context)

        res = printer.print_report_x()

        if res:
            data = self.browse(cr, uid, ids[0], context=context)
            lines = []
            for line in data.line_ids:
                lines.append({
                    'journal_id': int(line.journal_id),
                    'instrument_id': line.instrument_id.id,
                    'amount': line.amount,
                })
            values = {}
            values['number'] = res.get('report_number')
            values['printer_serial'] = res.get('printer_serial')
            values['pos_session_id'] = data.pos_session_id.id
            values['cashier_session_id'] = data.cashier_session_id.id
            values['lines'] = lines
            obj = self.pool.get('cash.count.reportx')
            obj.create_from_ui(cr, uid, values, context=context)
            return {
                'name': _('Your Session'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'pos.session.opening',
                'target': 'inline',
                'view_id': False,
                'type': 'ir.actions.act_window',
            }


class wizard_reportx_line(osv.osv_memory):
    _name = "wizard.reportx.line"

    def _get_journals(self, cr, uid, context=None):
        context = context or {}
        result = []
        if context.get('active_id'):
            sop_id = context.get('active_id')
            sop_obj = self.pool.get('pos.session.opening')
            sop = sop_obj.browse(cr, uid, sop_id, context=context)
            for s in sop.pos_session_id.statement_ids:
                result.append((s.journal_id.id, s.journal_id.name))
        return sorted(set(result))

    def onchange_journal(self, cr, uid, ids, journal_id, context=None):
        context = context or {}
        vals = {}
        if journal_id:
            obj = self.pool.get('account.journal')
            journal = obj.browse(cr, uid, journal_id, context=context)
            vals.update({'type': journal.type, 'instrument_id': ''})
        return {'value': vals}

    def _check_line_uniqueness(self, cr, uid, ids, context=None):
        context = context or {}
        data = self.browse(cr, uid, ids[0], context=context)
        c = [('reportx_id', '=', data.reportx_id.id), 
             ('journal_id', '=', int(data.journal_id)),
             ('instrument_id', '=', data.instrument_id.id)]
        result = self.search(cr, uid, c, context=context)
        return len(result) <= 1

    _columns = {
        'reportx_id': fields.many2one('wizard.reportx', 'Report'),
        'journal_id': fields.selection(_get_journals, 'Journal', required=True),
        'type': fields.char('Type', size=64),
        'instrument_id': fields.many2one('payment_instrument.instrument',
                                         'Payment Instrument'),
        'amount': fields.float('Amount',
                               required=True,
                               digits_compute=dp.get_precision('Account')),
    }

    _constraints = [
        (_check_line_uniqueness,_("Duplicated Payment Instrument"), [])

    ]
