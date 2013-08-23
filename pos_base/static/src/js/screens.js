function pos_base_screens(instance,module){

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

}