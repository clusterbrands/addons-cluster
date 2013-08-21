function payment_instrument_widgets(instance, module){

    module.PosWidget.include({
        build_widgets: function(){
            this._super();
            var self = this;               
            this.bank_selector = new module.BankSelectorPopup(this, {});
            this.bank_selector.appendTo($('.point-of-sale'));            
            this.screen_selector.add_popup('bank-selector',this.bank_selector);

            this.instrument_selector = new module.InstrumentSelectorPopup(this, {});
            this.instrument_selector.appendTo($('.point-of-sale'));            
            this.screen_selector.add_popup('instrument-selector',this.instrument_selector);
        }
    });

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
            added = new Array()
            _(payment_instruments).each(function(instrument) {
                if (_.indexOf(added,instrument.type) == -1){
                    var button = new module.PaypadInstrumentButtonWidget(self,{
                        pos: self.pos,
                        pos_widget : self.pos_widget,
                        instrument: instrument,
                    });
                    button.appendTo(self.$el);
                    added.push(instrument.type);
                }                
            });
        }
    });

    module.PaypadInstrumentButtonWidget = module.PosBaseWidget.extend({
        template:'PaypadInstrumentButtonWidget',
        events:{
            "click":"onClick",
        },
        init: function(parent, options){
            this._super(parent, options);            
            this.instrument = options.instrument;
        },
        onClick: function(){
            this.pos.set("instrument_type",this.instrument.type);
            this.pos_widget.screen_selector.show_popup('bank-selector');
        }
    });
}