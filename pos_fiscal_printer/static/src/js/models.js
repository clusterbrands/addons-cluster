function openerp_pos_models_ex(instance, module){
       
    _super = module.PosModel
    module.PosModel = module.PosModel.extend({
        initialize : function(session, attributes) {
            _super.prototype.initialize.call(this,session, attributes)
            this.db.clear('products','categories','customers');
            this.set({'customers':new module.CustomerCollection()});
        },
        load_server_data : function(){
            self = this
            loaded = _super.prototype.load_server_data.call(this)
                .then(function(){
                     return self.fetch('res.partner', ['name','vat','email',
                        'phone','mobile','street','street2'],[['customer', '=', true]]);
                }).then(function(customers){
                    self.db.add_customers(customers);
                    return self.fetch('pos.config',['printer_id'],
                        [['id','=', self.get('pos_session').config_id[0]]])
                }).then(function(config){
                    return self.fetch('pos_fiscal_printer.printer',
                        ['brand','name','port','serial','model',
                        'payment_method_ids','tax_rate_ids',
                        'measure_unit_ids'],
                        [['id','=',config[0].printer_id[0]]])
                }).then(function(printer){
                    self.get('pos_config').printer = printer[0]
                    if (printer[0]){
                        return self.fetch('pos_fiscal_printer.tax_rate', 
                            ['account_tax_id','code'],
                            [['printer_id','=',self.get('pos_config').printer.id]]
                        ).then(function(tax_rates){                
                            self.get('pos_config').printer.tax_rates = tax_rates
                            return self.fetch('pos_fiscal_printer.payment_method',
                                ['account_journal_id','code'],
                                [['printer_id','=',self.get('pos_config').printer.id]])
                        }).then(function(payment_methods){
                            self.get('pos_config').printer.payment_methods = payment_methods
                            return self.fetch('pos_fiscal_printer.measure_unit',
                                ['product_uom_id','code'],
                                [['printer_id','=',self.get('pos_config').printer.id]])
                        }).then(function(measure_units){
                            self.get('pos_config').printer.measure_units = measure_units
                        })
                    }
                })
                
            return loaded
        }
        
    })
        
    _super2 = module.Order
    module.Order = module.Order.extend({
       addPaymentLine: function(cashRegister) {
            //console.debug(this.pos.get('pos_config'))
            var paymentLines = this.get('paymentLines');
            var newPaymentline = new module.Paymentline({},
                                    {cashRegister:cashRegister,pos:this.pos});
            if(cashRegister.get('journal').type !== 'cash'){
                newPaymentline.set_amount( this.getDueLeft() );
            }
            paymentLines.add(newPaymentline);
        },
        export_for_printing : function(){
            order = _super2.prototype.export_for_printing.call(this);
            client  = this.get('client');
            printer = this.pos.get('pos_config').printer;
            street =  client ? client.street:""
            street2 = client ? client.street2:""
            order['client'] = {
                vat: client ? client.vat:"",
                name: order['client'],
                address : street + " " + street2,
            }
            order['printer'] = {
                model : printer.model[1],
                brand : printer.brand[1],
                port : printer.port,
                serial : printer.serial
            }
            return order;
        }
    })
    //Warning: this work just with one tax
    _super3 = module.Orderline
    module.Orderline = module.Orderline.extend({
        export_for_printing : function(){          
            product = this.get_product();
            taxes_ids = product.get('taxes_id');        
            tax_rates = this.pos.get('pos_config').printer.tax_rates;       
            _.each(taxes_ids,function(tax_id){
                tax = _.detect(tax_rates,function(t){
                            return t.account_tax_id[0] == tax_id
                        })            
            })
            uom_id = product.get('uom_id')[0]
            measure_units = this.pos.get('pos_config').printer.measure_units;
            
            unit = _.detect(measure_units,function(u){
                        return u.product_uom_id[0] == uom_id
                    })            
            order_line = _super3.prototype.export_for_printing.call(this);    
            order_line.tax_code = tax.code
            order_line.unit_code = unit.code
            return order_line
        }
    })
    
    _super4 = module.Paymentline
    module.Paymentline = module.Paymentline.extend({    
        initialize : function(attributes, options){
            _super4.prototype.initialize.call(this,attributes, options)
            this.pos = options.pos
        },
        export_for_printing : function(){
           account_journal_id = this.cashregister.get('journal_id')[0]
           payment_methods = this.pos.get('pos_config').printer.payment_methods;
           payment_method = _.detect(payment_methods,function(p){
                                return p.account_journal_id[0] == account_journal_id
                            })  
           payment_line = _super4.prototype.export_for_printing.call(this)
           payment_line.payment_method_code = payment_method.code
           return payment_line
        }
    })
    
    module.Customer = Backbone.Model.extend({
    });

    module.CustomerCollection = Backbone.Collection.extend({
        model: module.Customer,
    });
}
