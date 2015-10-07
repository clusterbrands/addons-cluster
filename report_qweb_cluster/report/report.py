from openerp import api, models
from openerp.addons.report.models.report import Report
import openerp.addons.base.ir.ir_qweb as ir_qweb
from lxml import etree

class CustomReport(Report):
	def render(self, cr, uid, ids, template, values=None, context=None):
		context = context or {}
		values = values or {}
		user = self.pool['res.users'].browse(cr, uid, uid)
		qweb = self.pool.get('ir.qweb')
		values.update(user=user, company=user.company_id)
		qwebcontext = ir_qweb.QWebContext(cr, uid, values, context=context)
		document = '<?xml version="1.0" ?><templates>'
		document += user.company_id.qweb_header
		document +=  user.company_id.qweb_footer + '</templates>'
		qweb.load_document(document, '', qwebcontext)
		custom_header = qweb.render(cr, uid, 'custom_header', qwebcontext, context=context)
		custom_footer = qweb.render(cr, uid, 'custom_footer', qwebcontext, context=context)
		values.update(
			custom_header=custom_header,
			custom_footer=custom_footer
		)
		return super(CustomReport, self).render(cr, uid, ids, template, values, context=context)
