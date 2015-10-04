from openerp import api, models
from openerp.addons.report.models.abstract_report import AbstractReport

class AbstractReportInherit(AbstractReport):
	def render_html(self, cr, uid, ids, data=None, context=None):
		import pdb
		pdb.set_trace()
