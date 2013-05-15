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
            .then(function(partners){
                 return self.fetch('res.partner', ['name','vat','email',
                    'phone','mobile'], [['customer', '=', true]]);
            }).then(function(customers){
                console.debug(self.db)
                self.db.add_customers(customers);                    
                return self.fetch('account.tax', ['amount', 'price_include', 'type']);
            })
        return loaded
    }
      
    
    module.Customer = Backbone.Model.extend({
    });

    module.CustomerCollection = Backbone.Collection.extend({
        model: module.Customer,
    });
}
