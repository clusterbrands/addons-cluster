function payment_instrument_screens(instance,module){
    
    module.BankSelectorPopup = module.BasePopup.extend({
        template:"BankSelectorPopup",
        events:{
            "click button[name!='cancel']":"onClickBtnJournal",
            "click button[name='cancel']":"onClickBtnCancel",
        },
        init: function(parent, options){
            this._super(parent, options);
            this.type = options.type || ""; 
            this.instrument_journals = new Array();         
        },
        show: function(){     
            self = this;       
            payment_instruments = this.pos.get("payment_instruments");
            current_instruments = _(payment_instruments).filter(function(i) {
                return i.type == self.type;
            })
            this.instrument_journals= _.uniq(current_instruments,false,function(i){
                return i.journal_id;
            }); 
            this.renderElement();
        },
        onClickBtnJournal: function(e){
            var journal = this.$(e.currentTarget).attr('journal');
            instrument_selector = new module.InstrumentSelectorPopup(this,{type:this.type,journal:journal});
            instrument_selector.appendTo($('.point-of-sale'));
            instrument_selector.show();
            instrument_selector.on('done',this,this.InstrumentSelected);
        },
        onClickBtnCancel: function(){
            this.close();
            this.hide();
        },
        InstrumentSelected:function(instrument){
            this.trigger('done',instrument);
            this.onClickBtnCancel();
        }
    });
    /*
    module.InstrumentSelectorPopup = module.BasePopup.extend({
        template:"InstrumentSelectorPopup",
        events:{
            "click button[name!='cancel']":"onClickBtnInstrument",
            "click button[name='cancel']":"onClickBtnCancel",
        },
        init: function(parent, options){
            this._super(parent, options);
            this.type = options.type || "";
            this.journal = options.journal || "";
            this.instruments = new Array();           
        },
        show: function(){
            var self = this;
            this._super();
            payment_instruments = this.pos.get("payment_instruments");
            this.instruments = _(payment_instruments).filter(function(i) {
                return (i.type == self.type && i.journal_id == self.journal);
            });
            this.renderElement();
        },
        onClickBtnInstrument: function(e){
            var instrument_id = this.$(e.currentTarget).attr('instrument');
            payment_instruments = this.pos.get("payment_instruments");
            instrument = _(payment_instruments).find(function(i) {
                return i.id == instrument_id;
            })
            this.trigger('done',instrument);
            this.onClickBtnCancel();           
        },
        onClickBtnCancel: function(){
         
            this.close();
            this.hide();
        },
    });*/

}
