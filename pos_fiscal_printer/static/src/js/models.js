/*
***************************************************************************
*    Module Writen to OpenERP, Open Source Management Solution
*    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
*    All Rights Reserved
***************Credits******************************************************
*    Coded by: Eduardo Ochoa    <eduardo.ochoa@clusterbrands.com.ve>
*                               <elos3000@gmail.com>
*****************************************************************************
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

function pos_fiscal_printer_models(instance, module){
       
    var _super = module.PosModel
    module.PosModel = module.PosModel.extend({
        load_server_data : function(){
            self = this
            loaded = _super.prototype.load_server_data.call(this)
                .then(function(){
                    model = new instance.web.Model('fiscal_printer.printer')
                    return model.call('get_printer',[true,[]])
                })
                .then(function(printer){
                    self.proxy.set_printer(printer)
                    self.set('printer',printer)
                })                
            return loaded
        }
        
    })
        
    var _super2 = module.Order
    module.Order = module.Order.extend({
       
        set_fiscal_printer:function (fiscal_printer){
            this.fiscal_printer = fiscal_printer
        },
        
        set_invoice_printer: function(invoice_printer){
            this.invoice_printer = invoice_printer
        },
                
        addPaymentLine: function(cashRegister) {
            var paymentLines = this.get('paymentLines');
            var newPaymentline = new module.Paymentline({},
                                    {cashRegister:cashRegister,pos:this.pos});
            if(cashRegister.get('journal').type !== 'cash'){
                newPaymentline.set_amount( this.getDueLeft() );
            }
            paymentLines.add(newPaymentline);
        },
        exportAsJSON : function(){
            order = _super2.prototype.exportAsJSON.call(this);
            order['partner_id'] = this.get('client') ? this.get('client').id: undefined;
            order['fiscal_printer'] = this.fiscal_printer;         
            order['invoice_printer'] = this.invoice_printer;
            return order
        },
        export_for_printing : function(){
            order = _super2.prototype.export_for_printing.call(this);
            client  = this.get('client');
            street =  client ? client.street:""
            street2 = client ? client.street2:""
            order['client'] = {
                vat: client ? client.vat:"",
                name: order['client'],
                address : street + " " + street2,
            }
            return order;
        }
    })
    //Warning: this work just with one tax
    var _super3 = module.Orderline
    module.Orderline = module.Orderline.extend({
        export_for_printing : function(){          
            product = this.get_product();
            printer = this.pos.proxy.get_printer();
            taxes_ids = product.get('taxes_id');        
            tax_rates = printer.tax_rate_ids;
            tax = ""       
            _.each(taxes_ids,function(tax_id){
                tax = _.detect(tax_rates,function(t){
                            return t.account_tax_id[0] == tax_id
                        }) 
            })
            uom_id = product.get('uom_id')[0]
            measure_units = printer.measure_unit_ids;
            
            unit = _.detect(measure_units,function(u){
                        return u.product_uom_id[0] == uom_id
                    })            
            order_line = _super3.prototype.export_for_printing.call(this);    
            order_line.tax_code = tax != "" ? tax.code:tax
            order_line.unit_code = unit ? unit.code:""
            return order_line
        }
    })
    
    var _super4 = module.Paymentline
    module.Paymentline = module.Paymentline.extend({    
        initialize : function(attributes, options){
            _super4.prototype.initialize.call(this,attributes, options)
            this.pos = options.pos
        },
        export_for_printing : function(){
            printer = this.pos.proxy.get_printer();
            account_journal_id = this.cashregister.get('journal_id')[0]
            payment_methods = printer.payment_method_ids;
            payment_method = _.detect(payment_methods,function(p){
                                return p.account_journal_id[0] == account_journal_id
                            })  
            payment_line = _super4.prototype.export_for_printing.call(this)
            payment_line.payment_method_code = payment_method ? payment_method.code:""
            return payment_line
        }
    })
    

}
