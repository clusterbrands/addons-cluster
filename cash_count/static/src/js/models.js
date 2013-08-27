function cash_count_models(instance, module){
    module.PosModel = module.PosModel.extend({
        load_server_data : function(){
            var self = this
            var loaded = this._super()
                .then(function(){
                    return self.fetch("cash.count.cashier",null,null)
                }).then(function(cashiers){
                    self.set('cashiers',cashiers);
                });
            return loaded;
        },
    });


    module.Session = Backbone.Model.extend({
        defaults:{
            "login_date": instance.web.datetime_to_str(new Date()),
        },
    });


}