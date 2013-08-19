function payment_instrument_widgets(instance, module){
    
    module.PaypadWidget.include({
        renderElement: function(){
            var self = this;
            this._super();
            this.$el.empty();
            this.pos.get('cashRegisters').each(function(cashRegister) {
                if (cashRegister.get("journal").type == 'cash'){
                    var button = new module.PaypadButtonWidget(self,{
                        pos: self.pos,
                        pos_widget : self.pos_widget,
                        cashRegister: cashRegister,
                    });
                    button.appendTo(self.$el);
                }
            });
            payment_instruments = this.pos.get('payment_instruments');
            _(payment_instruments).each(function(instrument) {
                console.debug(instrument)
                var button = new module.PaypadInstrumentButtonWidget(self,{
                    pos: self.pos,
                    pos_widget : self.pos_widget,
                    instrument: instrument,
                });
                button.appendTo(self.$el);  
            })
        }
    });

    module.PaypadInstrumentButtonWidget = module.PosBaseWidget.extend({
        template:'PaypadInstrumentButtonWidget',
        init: function(parent, options){
            this._super(parent, options);
            this.instrument = options.instrument;
        },
        template: 'PaypadInstrumentButtonWidget',
    })
}