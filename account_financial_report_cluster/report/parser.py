from openerp.osv import osv
from openerp.tools.translate import _
from openerp.report import report_sxw
from openerp.addons.account_financial_report.report.parser import AccountBalance 
from openerp.tools.safe_eval import safe_eval as eval

class account_balance_cluster(AccountBalance):

    def __init__(self, cr, uid, name, context):
        super(account_balance_cluster, self).__init__(cr, uid, name, context)
        self.context = context

    def lines(self, form, level=0):
        lines = super(account_balance_cluster, self).lines(form, level)
        lines2 = []
        for line in lines:
            if form['hide_views'] and line['type'] == 'view' and line['label']==True:
                continue
            if line['total'] and line['label'] == False and form['partial_sumarize'] == False and  line.has_key('level'):
                continue
            import pdb
            pdb.set_trace()
            lines2.append(line)
        return lines2

report_sxw.report_sxw('report.afr.rml.2cols2',
                     'wizard.report',
                     'addons/account_financial_report_cluster/report/balance_full_2_cols.rml',
                     parser=account_balance_cluster,
                     header=False)
