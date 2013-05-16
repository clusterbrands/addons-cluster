function openerp_pos_models_ex(instance, module){
       
    var _super_ = module.PosModel.prototype.initialize
    module.PosModel.prototype.initialize = function(session, attributes) {
        _super_.call(this,session, attributes)
        this.db.clear('products','categories','customers');
        this.set({'customers':new module.CustomerCollection()});
    }
    var _super2_ = module.PosModel.prototype.load_server_data
    module.PosModel.prototype.load_server_data= function(){
        self = this
        loaded = _super2_.call(this)
            .then(function(){
                 return self.fetch('res.partner', ['name','vat','email',
                    'phone','mobile','street','street2'],[['customer', '=', true]]);
            }).then(function(customers){
                self.db.add_customers(customers);
                return self.fetch('pos.config',['printer_id'],
                    [['id','=', self.get('pos_session').config_id[0]]])
            }).then(function(config){
                return self.fetch('pos_fiscal_printer.printer',
                    ['brand','name','port','serial','payment_method_ids',
                    'tax_rate_ids','measure_unit_ids'],
                    [['id','=',config[0].printer_id[0]]])
            }).then(function(printer){
                self.get('pos_config').printer = printer[0]
                return self.fetch('pos_fiscal_printer.tax_rate',
                    ['account_tax_id','code'],
                    [['printer_id','=',self.get('pos_config').printer.id]])
            }).then(function(tax_rates){                
                self.get('pos_config').printer.tax_rates = tax_rates
                return self.fetch('pos_fiscal_printer.payment_method',
                    ['account_journal_id','code'],
                    [['printer_id','=',self.get('pos_config').printer.id]])
            }).then(function(payment_methods){
                console.debug( self.get('pos_config').printer.tax_rates)
                self.get('pos_config').printer.payment_methods = payment_methods
                return self.fetch('pos_fiscal_printer.measure_unit',
                    ['product_uom_id','code'],
                    [['printer_id','=',self.get('pos_config').printer.id]])
            }).then(function(measure_units){
                self.get('pos_config').printer.measure_units = measure_units
            })
        
                
        return loaded
    }
    
    var _super3_ = module.Order.prototype.export_for_printing
    module.Order.prototype.export_for_printing = function(){
        order = _super3_.call(this);
        client  = this.get('client');
        order['client_vat'] = client ? client.vat:null
        order['client_street'] = client ? client.street:null
        order['client_street2'] = client ? client.street2:null
        return order;
    }
    //Warning: this work just with one tax
    var _super4_ = module.Orderline.prototype.export_for_printing
    module.Orderline.prototype.export_for_printing = function(){
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
        order_line = _super4_.call(this)        
        order_line.tax_code = tax.code
        order_line.unit_code = unit.code
        return order_line
    }
    
    var _super5_ = module.Paymentline.prototype.export_for_printing
    module.Paymentline.prototype.export_for_printing = function(){

       account_journal_id = this.cashregister.get('journal_id')[0]
       console.debug(this.pos)
       return _super5_.call(this)
    }
    
    var _super6_ = module.Paymentline.prototype.initialize
    module.Paymentline.prototype.initialize = function(attributes, options){
       _super6_.call(this,attributes, options)
        this.pos = options.pos
    }
    
    module.Customer = Backbone.Model.extend({
    });

    module.CustomerCollection = Backbone.Collection.extend({
        model: module.Customer,
    });
}
