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
                    journals = self.get("journals");
                    //if exist a cash journal add cash instrument to list
                    cash_journal = _(journals).find(function(j){return j.type == "cash";});
                    if (cash_journal){
                        instruments.push({
                            id : -1,
                            name : 'Cash',
                            type : 'cash',
                            type_desc: 'Cash',
                            code : 'CSH',
                            journal_id : [cash_journal.id,cash_journal.name],
                        });
                    }
                    _(instruments).each(function(instrument){
                        journal = _(journals).find(function(j) {
                            return j.id == instrument.journal_id[0]
                        })
                        self.fetch(                                                              
                            'account.bank.statement',                                                   
                            ['id'], [['state','=','open'], ['journal_id','=',journal.id], 
                                    ['pos_session_id', '=', self.get('pos_session').id], 
                                    ['instrument_id','=',instrument.id]]
                        ).then(function(stm){
                           instrument.statement_id = stm[0].id;
                        });
                        instrument.journal_name = journal.name;
                        instrument.journal_id = journal.id;
                        instrument.journal_image = instance.session.url('/web/binary/image', {model: 'account.journal', field: 'image_small', id: journal.id});
                        instrument.image = instance.session.url('/web/binary/image', {model: 'payment_instrument.instrument', field: 'image_small', id: instrument.id});
                    })
                    self.set("payment_instruments",instruments);
                })
            return loaded;
        }
    });
    
    module.Paymentline = module.Paymentline.extend({
        export_as_JSON: function(){
            var self = this;
            data = this._super();
            instrument = self.cashregister.get("instrument");
            if (instrument)
                _(data).extend({
                    "instrument_id": instrument.id,
                    "statement_id": instrument.statement_id,
                });
            return data;

        },
        export_for_printing: function(){
            var self = this;
            data = this._super();
            instrument = self.cashregister.get("instrument");
            if (instrument)
                _(data).extend({
                    "journal": data.journal + ' ' + instrument.code,
                });
            return data;
        },
    })
}
