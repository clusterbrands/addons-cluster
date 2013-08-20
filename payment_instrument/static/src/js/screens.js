function payment_instrument_screens(instance,module){

    module.ScreenSelector.include({
        add_popup: function(popup_name, popup){
            popup.hide();
            this.popup_set[popup_name] = popup;
            return this;
        },
    })   

    module.BasePopup = module.PopUpWidget.extend({
        template:"BasePopup",
        events:{
            "click a.close":"closePopup",
        },
        init: function(parent, options){
            this._super(parent, options);
        },    
        renderElement: function(){
            this._super();
            this.$('.popup').position({my:"center",of:".point-of-sale"});
            this.$('.popup').draggable();
        },
        closePopup:function(e){
            this.close();
            this.hide();
        },       
        
    });

    module.BankSelectorPopup = module.BasePopup.extend({
        template:"BankSelectorPopup",
        init: function(parent, options){
            this._super(parent, options);
            this.journals = new Array('uno','dos','tres')
            console.debug(this.$el);
            
        },
        show: function(){
            this._super();
            this.load_data()
            this.renderElement();
        },
        load_data: function(){            
            current_type = this.pos.get("instrument_type");
            payment_instruments = this.pos.get("payment_instruments");
            current_instruments = _(payment_instruments).filter( function(instrument) {
                return instrument.type == current_type;              
            });
            this.journals = _(current_instruments).groupBy( function(instrument) {
                return instrument.journal_id[1];
            });
        },
    });

}