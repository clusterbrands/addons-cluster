function payment_instrument_widgets(instance, module){

    var _renderElement =  module.PosBaseWidget.prototype.renderElement;
    module.PaypadWidget.include({
        events:{
            "click button[type='cash']":"onClickBtnCash",
            "click button[type!='cash']":"onClickBtnOther",
        },
        init: function(parent,options){
            this._super(parent,options);
            this.instrument_types = new Array();
        },
        renderElement: function(){
            var self = this;
            payment_instruments = this.pos.get('payment_instruments');
            this.instrument_types = _.uniq(payment_instruments,false,function(i){
                return i.type;
            });           
            _renderElement.call(this);
        },
        onClickBtnCash: function(e){
            payment_instruments = this.pos.get('payment_instruments');
            var instrument = _(payment_instruments).find(function(i) {
                return i.type == "cash";
            })
            this.onInstrumentCashSelected(instrument);
        },
        onClickBtnOther: function(e){
            var type = this.$(e.target).attr('type');
            bank_selector = new module.BankSelectorPopup(this,{type:type});
            bank_selector.appendTo($('.point-of-sale'));
            bank_selector.show();
            bank_selector.on('done',this,this.onInstrumentOtherSelected);
        },
        onInstrumentCashSelected : function(instrument){
            cash_registers = self.pos.get("cashRegisters");
            cash_register = _(cash_registers.models).find(function(c) {
                return c.get("journal").id == instrument.journal_id
            })
            this.pos.get('selectedOrder').addPaymentLine(cash_register);
            this.pos_widget.screen_selector.set_current_screen('payment');
        },
        onInstrumentOtherSelected: function(instrument){
            cash_registers = this.pos.get("cashRegisters");
            cash_register = _(cash_registers.models).find(function(c) {
                return c.get("journal").id == instrument.journal_id
            })

            var cr = cash_register.clone();
            cr.set("instrument",instrument);
            this.pos.get('selectedOrder').addPaymentLine(cr);
            this.pos_widget.screen_selector.set_current_screen('payment');
        }

    });
}