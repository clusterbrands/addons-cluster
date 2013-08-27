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
            this.closeable = _(options).has('closeable') ? options.closeable : true; 
            this.draggable = _(options).has('draggable') ? options.draggable : true; 
        }, 
        start: function(){
            this.renderElement();
        },   
        renderElement: function(){
            this._super();
            this.$("a.close").off('click').click(_.bind(this.closePopup,this));
            this.$('.popup').position({my:"center",of:".point-of-sale"});
            if (this.draggable)
                this.$('.popup').draggable();
        },
        closePopup:function(e){
            this.close();
            this.hide();
        },       
    });   

    module.Alert = module.BasePopup.extend({
        template:'Alert',
        init: function(parent,options){
            this._super(parent,options);
            this.title = options.title || "";
            this.msg = options.msg || "";
        },
        renderElement:function(){
            this._super();
            this.$('button').off('click').click(_.bind(this.onClickBtn,this));
            this.$('button').focus();
        },
        onClickBtn: function(){
            this.close();
            this.hide();
            this.trigger('continue');
        }
    })

}