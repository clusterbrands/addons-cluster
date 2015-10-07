1 #!/usr/bin/python
 # -*- encoding: utf-8 -*-
 #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 #    Module Writen to OpenERP, Open Source Management Solution
 #    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
 #    All Rights Reserved
 #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 #    Author: Cluster Brands
 #    Copyright 2013 Cluster Brands
 #    Designed By: Jose J Perez M <jose.perez@clusterbrands.com>
 #    Coded by: Eduardo Ochoa  <eduardo.ochoa@clusterbrands.com.ve>
 #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 #    This program is free software: you can redistribute it and/or modify
 #    it under the terms of the GNU Affero General Public License as published
 #    by the Free Software Foundation, either version 3 of the License, or
 #    (at your option) any later version.
 #    This program is distributed in the hope that it will be useful,
 #    but WITHOUT ANY WARRANTY; without even the implied warranty of
 #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #    GNU Affero General Public License for more details.
 #
 #    You should have received a copy of the GNU Affero General Public License
 #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from openerp.osv import osv, fields
from openerp import api

class res_company(osv.osv):
    _inherit = "res.company"

    def _get_default_header(self, cr, uid, context):
		res ="""<div t-name="custom_header" class="header">
    <div class="row">
        <div class="col-xs-3">
        	<img t-if="company.logo" t-att-src="'data:image/png;base64,%s' % company.logo" class="company-logo"/>
        </div>
        <div class="col-xs-9 text-right" style="margin-top:20px;" t-field="company.rml_header1"/>
     </div>
     <div class="row zero_min_height">
        <div class="col-xs-12">
        	<div style="border-bottom: 1px solid black;"></div>
        </div>
     </div>
     <div class="row">
    	 <div class="col-xs-3">
        	 <div t-field="company.partner_id" 
                  t-field-options='{"widget": "contact", "fields": ["address", "name"], "no_marker": true}'
                  style="border-bottom: 1px solid black;"/>
         </div>
     </div>
</div>"""
		return res

    def _get_default_footer(self, cr, uid, context):
		res ="""<div t-name="custom_footer" class="footer">
    <div class="text-center" style="border-top: 1px solid black;">
        <ul t-if="not company.custom_footer" class="list-inline">
            <li t-if="company.phone">Phone: <span t-field="company.phone"/></li>
            <li t-if="company.fax and company.phone">&amp;bull;</li>
            <li t-if="company.fax">Fax: <span t-field="company.fax"/></li>
            <li t-if="company.email">&amp;bull;</li>
            <li t-if="company.email">Email: <span t-field="company.email"/></li>
            <li t-if="company.website">&amp;bull;</li>
            <li t-if="company.website">Website: <span t-field="company.website"/></li>
        </ul>
        <t t-if="company.custom_footer">
	        <span t-raw="company.rml_footer"/>
        </t>
        <ul class="list-inline">
            <li>Page:</li>
            <li><span class="page"/></li>
            <li>/</li>
            <li><span class="topage"/></li>
        </ul>
    </div>
</div>
"""
		return res

    _columns = {
    	'qweb_header': fields.text('Report Header', help="Custom Header for all reports"), 
		'qweb_footer': fields.text('Report Footer', help="Custom Footer for all reports"),
		'qweb_style' : fields.text('Report Style', help="Custom Style")
    }

    _defaults = {
    	'qweb_header': _get_default_header,
    	'qweb_footer': _get_default_footer,
    }
