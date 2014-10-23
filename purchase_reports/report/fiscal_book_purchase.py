# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from openerp.report import report_sxw
from openerp.osv import osv

class fiscal_book_purchase(report_sxw.rml_parse):
   def __init__(self, cr, uid, name, context):
      super(fiscal_book_purchase, self).__init__(cr, uid, name, context=context)
      self.localcontext.update({
         'get_tax': self.get_tax,
      })
      self.context = context

   def get_tax(self, fbl):
      tax = '';
      if fbl.vat_general_tax:
         tax = '12%'
      elif fbl.vat_reduced_tax:
         tax = '8%'
      elif fbl.vat_additional_tax:
         tax = '22%'
      return tax 
 

report_sxw.report_sxw('report.fiscal.book.purchase','fiscal.book','addons/purchase_reports/report/fiscal_book_purchase.rml',parser=fiscal_book_purchase)