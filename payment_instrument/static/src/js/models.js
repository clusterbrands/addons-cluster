function payment_instrument_models(instance, module) {
    module.PosModel = module.PosModel.extend({        
        load_server_data : function(){
            var self = this;         
            var loaded = this._super()
                 .then(function(){
                    return self.fetch(
                        'account.bank.statement',
                        ['account_id','currency','journal_id','state','name','user_id','pos_session_id','instrument_id'],
                        [['state','=','open'],['pos_session_id', '=', self.get('pos_session').id]]
                    );
                }).then(function(bank_statements){
                    self.set('bank_statements',bank_statements);
                    var instruments = new Array();
                    _(bank_statements).each(function(bank_statement) {
                        if (bank_statement.instrument_id)
                            instruments.push(bank_statement.instrument_id[0]);
                    })    
                    return self.fetch('payment_instrument.instrument', undefined, [['id','in',instruments]]);
                }).then(function(instruments){
                    
                    var journals = self.get("journals");
                    var bank_statements = self.get('bank_statements');
                   
                    _(instruments).each(function(instrument){
                        journal = _(journals).find(function(j) {
                            return j.id == instrument.journal_id[0];
                        })
                        bank_statement = _(bank_statements).find(function(b) {
                            return b.instrument_id[0] == instrument.id;
                        })
                        instrument.statement_id = bank_statement.id;
                        instrument.journal_name = journal.name;
                        instrument.journal_id = journal.id;
                        instrument.journal_image = instance.session.url('/web/binary/image', {model: 'account.journal', field: 'image_small', id: journal.id});
                        instrument.image = instance.session.url('/web/binary/image', {model: 'payment_instrument.instrument', field: 'image_small', id: instrument.id});
                    })
                    //if exist a cash journal add cash instrument to list
                    cash_journal = _(journals).find(function(j){return j.type == "cash";});
                    if (cash_journal){
                        instruments.push({
                            id : -1,
                            name : 'Cash',
                            type : 'cash',
                            type_desc: 'Cash',
                            code : 'CSH',
                            journal_id : cash_journal.id,
                        });
                    }
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
