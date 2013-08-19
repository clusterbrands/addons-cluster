openerp.payment_instrument = function(instance) {
   var module = instance.point_of_sale;

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
               instrument_ids = _.flatten(instruments);
               return self.fetch('payment_instrument.instrument', undefined, [['id','in', instrument_ids]]);
            }).then(function(instruments){
               cash_registers = self.get("cashRegisters")
               cash_registers.each(function(register){
                  register.get("journal").payment_instrument_ids = new Array() 
                  _(instruments).each(function(instrument){
                     if (register.get("journal").id == instrument.journal_id[0]){
                        aux = [instrument.id,instrument.name];
                        register.get("journal").payment_instrument_ids.push(aux);
                     }
                  })
               })
            })
         return loaded;
      }
   })
}