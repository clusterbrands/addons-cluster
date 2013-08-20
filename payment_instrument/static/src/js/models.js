function payment_instrument_models(instance, module) {
    module.PosModel = module.PosModel.extend({        
        load_server_data : function(){
            var self = this;         
            var loaded = this._super()
                .then(function(){
                    instruments = new Array();
                    journals = self.get("journals");
                    _(journals).each(function(journal) {
                        instruments.push(journal.payment_instrument_ids);
                    })       
                    return self.fetch('payment_instrument.instrument', undefined, [['id','in',_.flatten(instruments)]]);
                }).then(function(instruments){
                    self.set("payment_instruments",instruments);
                })
            return loaded;
        }
    })
}