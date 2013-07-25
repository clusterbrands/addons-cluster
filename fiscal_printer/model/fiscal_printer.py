#!/usr/bin/python
# -*- encoding: utf-8 -*-
#
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved Credits
#
#    Coded by: Eduardo Ochoa    <eduardo.ochoa@clusterbrands.com.ve>
#                               <elos3000@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from openerp.osv.orm import except_orm, BaseModel
from openerp.osv import osv, fields
from openerp.tools.translate import _

class proxy (osv.Model):

    _name = 'fiscal_printer.proxy'
    _columns = {
        'connection_name': fields.char('Connection Name', size=255,
                                       required=True),
        'url': fields.char('Local Proxy Url', size=255,
                           required=True)
    }


class brand(osv.Model):

    _name = 'fiscal_printer.brand'
    _rec_name = 'name'
    _columns = {
        'name': fields.char(size=50)
    }


class model(osv.Model):

    _name = 'fiscal_printer.model'
    _rec_name = 'name'
    _columns = {
        'name': fields.char(size=50),
        'brand_id': fields.many2one('fiscal_printer.brand')
    }


class printer(osv.Model):
    
    _inherit = "generic.device"
    _name = 'fiscal_printer.printer'
    
    def _get_cpath(self, cr, uid, context=None):
        return "/fiscal_printer";
        
    def get_assigned_printer(self, cr, uid, ids, context=None):
        wrk = self.read_workstation(cr, uid, ids, context=context)
        printer_id = self.search(cr, uid, [('workstation', '=', wrk),
                                 ('enabled', '=', True)])
        if printer_id:
            return self.browse(cr, uid, printer_id)[0]
        else:
            return {}

    def get_assigned_printer_web(self, cr, uid, ids, context=None):
        printer = {}
        wrk = self.read_workstation(cr, uid, ids, context=context)
        printer_id = self.search(cr, uid, [('workstation', '=', wrk),
                                 ('enabled', '=', True)])
        if printer_id:
            data = self.browse(cr, uid, printer_id, context=context)[0]
            taxes = [{"account_tax_id":tax.account_tax_id, 
                      "code":tax.code} for tax in data.tax_rate_ids]

            payments = [{"account_journal_id":payment.account_journal_id,
                        "code":payment.code}
                        for payment in data.payment_method_ids]

            uoms = [{"product_uom_id":uom.product_uom_id,
                    "code":uom.code} for uom in data.measure_unit_ids]

            printer.update({
                "name": data.name,
                "brand": data.brand.brand_name,
                "model": data.model.model_name,
                "port": data.port,
                "serial": data.serial,
                "tax_rates": taxes,
                "payment_methods": payments,
                "meansure_units": uoms
            })
        return printer

    def read_workstation(self, cr, uid, ids, context=None):
        context = context or {}
        response = self.send_command(cr, uid, ids, 'read_workstation',
                                     context=context)
        return response.get('workstation') or ""

    def read_payment_methods(self, cr, uid, ids, context=None):
        context = context or {}
        response = self.send_command(cr, uid, ids, 'read_payment_methods',
                                     context=context)

    def write_payment_methods(self, cr, uid, ids, context=None):
        context = context or {}
        payment_methods = []
        printer = self.browse(cr, uid, ids)[0]
        for pm in printer.payment_method_ids:
            payment_methods.append({'code': str(pm.code),
                                    'description': str(pm.description)})
        params = {'payment_methods': payment_methods}
        response = self.send_command(cr, uid, ids, 
                                     'write_payment_methods', params,
                                     context=context)

    def read_tax_rates(self, cr, uid, ids, context=None):
        context = context or {}
        tax_rates = {}
        response = self.send_command(cr, uid, ids, 'read_tax_rates',
                                     context=context)
        tax_rates = response.get('tax_rates')
        obj = self.pool.get('fiscal_printer.tax_rate')
        for tr in tax_rates:
            tax_id = obj.search(cr, uid, [('code', '=', tr.get('code'))],
                                context=context)
            if not tax_id:
                vals = {'printer_id': ids[0],
                        'current_value': tr.get('value'),
                        'value': tr.get('value'),
                        'description': tr.get('description'),
                        'code': tr.get('code')
                        }
                obj.create(cr, uid, vals, context=context)
            else:
                obj.write(cr, uid, tax_id, {'current_value': tr.get('value')},
                          context=context)
        return True

    def write_tax_rates(self, cr, uid, ids, context=None):
        context = context or {}
        tax_rates = []
        printer = self.browse(cr, uid, ids)[0]
        for tax in printer.tax_rate_ids:
            tax_rates.append({'code': tax.code, 'value': tax.value})

        params = {'tax_rates': tax_rates}
        response = self.send_command(cr, uid, ids, 'write_tax_rates', 
                                     params,context=context)

    def read_headers(self, cr, uid, ids, context=None):
        context = context or {}
        response = self.send_command(cr, uid, ids, 'read_headers',
                                     context=context)
        headers = response.get('headers')
        obj = self.pool.get('fiscal_printer.header')
        for header in headers:
            if header.strip() != "":
                header_id = obj.search(
                    cr, uid, [('current_value', '=', header.rstrip())],
                    context=context)
                if not header_id:
                    vals = {'printer_id': ids[0],
                            'current_value': header.rstrip(),
                            'value': header.rstrip(),
                            }
                    obj.create(cr, uid, vals, context=context)
        return True

    def write_headers(self, cr, uid, ids, context=None):
        context = context or {}
        headers = []
        header_ids = []
        printer = self.browse(cr, uid, ids)[0]
        for header in printer.header_ids:
            if (header.value != header.current_value):
                headers.append(header.value)
                header_ids.append(header.id)
        params = {'headers': headers}
        response = self.send_command(cr, uid, ids, 'write_headers', params,
                                context=context)
        if (response.get('exec')):
            for id in header_ids:
                obj = self.pool.get('fiscal_printer.header')
                brw = obj.browse(cr, uid, id)
                obj.write(cr, uid, id, {'current_value': brw.value},
                          context=context)

    def read_footers(self, cr, uid, ids, context=None):
        context = context or {}
        response = self.send_command(cr, uid, ids, 'read_footers', 
                                     context=context)
        footers = response.get('footers')
        obj = self.pool.get('fiscal_printer.footer')
        for footer in footers:
            if footer.strip() != "":
                footer_id = obj.search(
                    cr, uid, [('current_value', '=', footer.rstrip())],
                    context=context)
                if not footer_id:
                    vals = {'printer_id': ids[0],
                            'current_value': footer.rstrip(),
                            'value': footer.rstrip(),
                            }
                    obj.create(cr, uid, vals, context=context)
        return True

    def write_footers(self, cr, uid, ids, context=None):
        context = context or {}
        footers = []
        footer_ids = []
        printer = self.browse(cr, uid, ids)[0]
        for footer in printer.footer_ids:
            if (footer.value != footer.current_value):
                footers.append(footer.value)
                footer_ids.append(footer.id)
        params = {'footers': footers}
        response = self.send_command(cr, uid, ids, 'write_footers',
                                     params, context=context)
        if (response.get('exec')):
            for id in footer_ids:
                obj = self.pool.get('fiscal_printer.footer')
                brw = obj.browse(cr, uid, id,context=context)
                obj.write(cr, uid, id, {'current_value': brw.value}, 
                          context=context)

    def read_serial(self, cr, uid, ids, context=None):
        context = context or {}
        response = self.send_command(cr, uid, ids, 'read_printer_serial',
                                     context=context)
        serial = response.get('serial')
        self.write(cr, uid, ids, {'serial': serial}, context=context)
        return True

    def _check_active_printer_uniqueness(self, cr, uid, ids, context=None):
        brw = self.browse(cr, uid, ids)[0]
        wrk = brw.workstation
        ids = self.search(
            cr, uid, [('workstation', '=', wrk), ('enabled', '=', True)])
        return len(ids) <= 1

    def default_get(self, cr, uid, fields, context=None):
        context = context or {}
        try:
            response = self.send_command(cr, uid, [],'get_supported_printers')
            printers = response
        except:
            return ""

        pb_obj = self.pool.get('fiscal_printer.brand')
        pm_obj = self.pool.get('fiscal_printer.model')
        for brand in printers:
            brand_id = pb_obj.search(cr, uid, [('name', '=', brand)],
                                     context=context)
            if not brand_id:
                brand_id = [pb_obj.create(cr, uid, {'name': brand},
                            context=context)]
            for model in printers[brand]:
                m = pm_obj.search(cr, uid, [('name', '=', model)],
                                  context=context, count=True)
                if (m == 0):
                    pm_obj.create(cr, uid, {'brand_id': brand_id[0],
                                            'name': model}, context)
        res = {}
        wrk = self.read_workstation(cr, uid, [], context=context)
        res.update({"workstation": wrk})
        return res

    _columns = {
        'name': fields.char(string='Name', size=50, required=True),
        'brand': fields.many2one('fiscal_printer.brand',
                                 string='Brand', required=True),
        'model': fields.many2one('fiscal_printer.model',
                                 string='Model', required=True),
        'port': fields.char(string='Port', size=100, required=True),
        'workstation': fields.char(string='Workstation', size=255, required=True, readonly=True),
        'type': fields.boolean('Ticket Printer'),
        'serial': fields.char(string='Serial', size=50),
        'enabled': fields.boolean(string="Active"),
        'payment_method_ids': fields.one2many('fiscal_printer.payment_method',
                                              'printer_id', string="Payment Methods"),
        'tax_rate_ids': fields.one2many('fiscal_printer.tax_rate',
                                        'printer_id', string="Tax Rates"),
        'measure_unit_ids': fields.one2many('fiscal_printer.measure_unit',
                                            'printer_id', string="Unit of Measure"),
        'header_ids': fields.one2many('fiscal_printer.header',
                                      'printer_id', string="Header"),
        'footer_ids': fields.one2many('fiscal_printer.footer',
                                      'printer_id', string="Footers"),
    }

    _constraints = [
        (_check_active_printer_uniqueness,
         _("Only one active printer allowed per workstation"), [])

    ]


class payment_method(osv.Model):

    _name = 'fiscal_printer.payment_method'
    _columns = {
        'printer_id': fields.many2one('fiscal_printer.printer'),
        'account_journal_id': fields.many2one('account.journal',
                                              string='Payment Method', domain=[('journal_user', '=', 'True')]),
        'code': fields.char(string='Code', size=2),
        'description': fields.char(string='Description', size=50),
        'current_description': fields.char(string='Current Description', size=50),
    }

    _defaults = {
        'current_description': lambda *a: "Not available"
    }


class tax_rate(osv.Model):

    _name = 'fiscal_printer.tax_rate'
    _columns = {
        'printer_id': fields.many2one('fiscal_printer.printer'),
        'account_tax_id': fields.many2one('account.tax',
                                          string='Tax', domain=[('type_tax_use', '=', 'sale')]),
        'code': fields.char(string='Tax Code', size=4),
        'description': fields.char(string='Description', size=255),
        'value': fields.float(digits=(12, 2), string='Value'),
        'current_value': fields.float(digits=(12, 2), string='Current Value'),
    }
    _defaults = {
        'current_value': lambda *a: 0.0
    }


class measure_unit (osv.Model):

    _name = 'fiscal_printer.measure_unit'
    _columns = {
        'printer_id': fields.many2one('fiscal_printer.printer'),
        'product_uom_id': fields.many2one('product.uom',
                                          string='Tax', domain=[('active', '=', 'True')]),
        'Name': fields.char(size=255, string='Name'),
        'current_code': fields.char(size=255, string='Current Code'),
        'code': fields.char(size=2, string='Code')
    }


class header(osv.Model):

    _name = 'fiscal_printer.header'
    _columns = {
        'printer_id': fields.many2one('fiscal_printer.printer'),
        'current_value': fields.char(size=255, string='Current Value'),
        'value': fields.char(size=255, string='Value')
    }

    _defaults = {
        'current_value': lambda *a: "Not available"
    }


class footer(osv.Model):

    _name = 'fiscal_printer.footer'
    _columns = {
        'printer_id': fields.many2one('fiscal_printer.printer'),
        'current_value': fields.char(size=255, string='Current Value'),
        'value': fields.char(size=255, string='Value')
    }

    _defaults = {
        'current_value': lambda *a: "Not available"
    }
