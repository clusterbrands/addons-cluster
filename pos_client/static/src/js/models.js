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
                    return self.fetch(
                        'pos.config',['country_id'],
                        [['id','=', self.get('pos_session').config_id[0]]]);
                }).then(function(config){
                     country_id = config[0].country_id[0]
                     return self.fetch('res.partner', ['name','vat','email',
                        'phone','mobile','street','street2','city','vat_subjected',
                        'wh_iva_agent','seniat_updated'],[['customer', '=', true],
                        ['vat','!=',''],['country_id','=',country_id]]);
                }).then(function(customers){
                    self.db.add_customers(customers);
                })
            return loaded
        },
        add_customer:function(custumer){
            this.db.add_customer(customer);
        },
    })
    
    module.Customer = Backbone.Model.extend({
        defaults:{
            vat:"",
            name:"",
            street:"",
            street2:"",
            phone:"",
            email:"",
            city:"",
            vat_subjected:null,
            wh_iva_agent:null,
            seniat_updated:null,
            create:false,
            update:false,       
        }
    });

    module.CustomerCollection = Backbone.Collection.extend({
        model: module.Customer,
    });
}
