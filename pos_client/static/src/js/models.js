function openerp_pos_models_ex(instance, module){
    
    _super = module.PosModel
    module.PosModel = module.PosModel.extend({
        initialize : function(session, attributes) {
            _super.prototype.initialize.call(this,session, attributes)
            this.db.clear('products','categories','customers','new-customers','updated-customer');
            this.set({'customers':new module.CustomerCollection()});
            this.set({'new-customers':new module.CustomerCollection()});
            this.set({'updated-customers':new module.CustomerCollection()});
        },
        load_server_data : function(){
            self = this
            loaded = _super.prototype.load_server_data.call(this)
                .then(function(){
                    return self.fetch(
                        'pos.config',['country_id'],
                        [['id','=', self.get('pos_session').config_id[0]]]);
                }).then(function(config){
                     country_id = config[0].country_id[0];
                     self.set({'country_id':country_id})
                     return self.fetch('res.partner', ['name','vat','email',
                        'phone','mobile','street','street2','city','vat_subjected',
                        'wh_iva_agent','seniat_updated'],[['customer', '=', true],
                        ['vat','!=',''],['country_id','=',country_id]]);
                }).then(function(customers){
                    self.db.add_customers(customers);
                })
            return loaded
        },
        create_customer:function(customer){
            this.db.add_customer(customer);
            this._flush_new_customers(0);
        },        
        update_customer:function(customer){
            this.db.update_customer(customer);
            this._flush_updated_customers(0);
        },
        _flush_new_customers: function(index){
            var self = this;
            var customers = this.db.get_new_customers();

            var customer  = customers[index];
            if(!customer){
                return;
            }
            //try to push an order to the server
            // shadow : true is to prevent a spinner to appear in case of timeout
            (new instance.web.Model('pos.client')).call('create_from_ui',[customer,self.get('country_id')],undefined,{ shadow:true })
                .fail(function(unused, event){
                    //don't show error popup if it fails 
                    event.preventDefault();
                    console.error('Failed to create customer:',customer);
                    self._flush_new_customers(index+1);
                })
                .done(function(){
                    //remove from db if success
                    self.db.remove_created_customer(customer.vat);
                    self._flush_new_customers(index);
                });
        },
        _flush_updated_customers: function(index){

            var self = this;
            var customers = this.db.get_updated_customers();

            var customer  = customers[index];
            if(!customer){
                return;
            }            
            //try to push an order to the server
            // shadow : true is to prevent a spinner to appear in case of timeout
            (new instance.web.Model('pos.client')).call('update_from_ui',[customer,self.get('country_id')],undefined,{ shadow:true })
                .fail(function(unused, event){
                    //don't show error popup if it fails 
                    event.preventDefault();
                    console.error('Failed to update customer:',customer);
                    self._flush_updated_customers(index+1);
                })
                .done(function(){
                    //remove from db if success
                    self.db.remove_updated_customer(customer.vat);
                    self._flush_updated_customers(index);
                });
        },
    })
    
    module.Customer = Backbone.Model.extend({
        defaults:{
            vat:"V",
            vat_subjected:false,
            wh_iva_agent:false,   
        },
        set: function(key,value,options) {
            options = options || {};
            if (!('silent' in options)) {
                options.silent = true;
            }
            return Backbone.Model.prototype.set.call(this,key,value,options);
        },
        getVatLetter: function(){
            return this.get('vat')[0];
        },
        getVatNumbers:function(){
            return  _.rest(this.get('vat'),1).join('');
        },
        setVatLetter:function(value){
            aux = value+_.rest(this.get('vat'),1).join('');
            this.set('vat',aux);
        },
        setVatNumbers:function(value){
            aux = this.getVatLetter()+value;
            this.set('vat',aux);
        }
    });

    module.CustomerCollection = Backbone.Collection.extend({
        model: module.Customer,
    });
}
