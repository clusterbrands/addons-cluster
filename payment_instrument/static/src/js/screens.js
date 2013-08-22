function payment_instrument_screens(instance,module){

    module.ScreenSelector.include({
        add_popup: function(popup_name, popup){
            popup.hide();
            this.popup_set[popup_name] = popup;
            return this;
        },
    });  

    module.BasePopup = module.PopUpWidget.extend({
        template:"BasePopup",
        init: function(parent, options){
            this._super(parent, options);
        },    
        renderElement: function(){
            this._super();
            this.$("a.close").off('click').click(_.bind(this.closePopup,this));
            this.$('.popup').position({my:"center",of:".point-of-sale"});
            this.$('.popup').draggable();
        },
        closePopup:function(e){
            this.close();
            this.hide();
        },       
        
    });

    module.BankActionButton = module.PosBaseWidget.extend({
        template:"BankActionButton",
        init: function(parent, options){
            this._super(parent, options);
            this.instrument = options.instrument;            
        },
        renderElement: function(){
            this._super();
            this.$el.click(_.bind(this.onClickButton,this));
        },
        onClickButton: function(){
            this.pos.set("instrument_journal",this.instrument.journal_id);
            this.pos_widget.screen_selector.show_popup('instrument-selector');
        }       
    });

    module.BankSelectorPopup = module.BasePopup.extend({
        template:"BankSelectorPopup",
        events:{
            "click button[name='cancel']":"onClickBtnCancel",
        },
        init: function(parent, options){
            this._super(parent, options);
            this.journals = new Array();            
        },
        show: function(){
            this._super();
            this.renderElement();
            this.load_data();
        },
        load_data: function(){     
            self = this;       
            current_type = this.pos.get("instrument_type");
            payment_instruments = this.pos.get("payment_instruments");
            var journals = new Array()
            var keys = new Array()
            _(payment_instruments).each(function(i){
                if (i.type == current_type)
                    if (_(keys).indexOf(i.journal_id)){
                        var button = new module.BankActionButton(self,{
                            pos: self.pos,
                            pos_widget : self.pos_widget,
                            instrument : i,
                        });
                        button.appendTo(self.$(".button-bar"));
                        keys.push(i.journal_id);
                    }
            }); 
        },
        onClickBtnCancel: function(){
            this.close();
            this.hide();
        },
    });

    module.InstrumentActionButton = module.PosBaseWidget.extend({
        template:"InstrumentActionButton",
        init: function(parent, options){
            this._super(parent, options);
            this.instrument = options.instrument;            
        },
        renderElement: function(){
            this._super();
            this.$el.click(_.bind(this.onClickButton,this));
        },
        onClickButton: function(){
            var self = this
            if (self.pos.get('selectedOrder').get('screen') === 'receipt'){  //TODO Why ?
                    console.warn('TODO should not get there...?');
                    return;
            }
            cash_registers = self.pos.get("cashRegisters");
            cash_register = _(cash_registers.models).find(function(c) {
                return c.get("journal").id == self.instrument.journal_id
            })
            journal_id = cash_register.get("journal_id")
            journal_id[1] = this.instrument.journal_name + " " + this.instrument.code ;
            cash_register.set("journal_id",journal_id); 
            cash_register.set("instrument_id",this.instrument.id);
            self.pos.get('selectedOrder').addPaymentLine(cash_register);
            self.pos_widget.screen_selector.set_current_screen('payment');
        }       
    });

    module.InstrumentSelectorPopup = module.BasePopup.extend({
        template:"InstrumentSelectorPopup",
        events:{
            "click button[name='cancel']":"onClickBtnCancel",
        },
        init: function(parent, options){
            this._super(parent, options);
            this.journals = new Array();            
        },
        show: function(){
            this._super();
            this.renderElement();
            this.load_data();
        },
        load_data: function(){     
            self = this;
            current_type = this.pos.get("instrument_type");
            current_journal = this.pos.get("instrument_journal");
            payment_instruments = this.pos.get("payment_instruments");
            _(payment_instruments).each(function(i){
                if (i.type == current_type){
                    if (i.journal_id == current_journal){
                        var button = new module.InstrumentActionButton(self,{
                            pos: self.pos,
                            pos_widget : self.pos_widget,
                            instrument : i,
                        });
                        button.appendTo(self.$(".button-bar"));
                    }
                }     
            });     
        },
        onClickBtnCancel: function(){
            this.close();
            this.hide();
        },
    });

}