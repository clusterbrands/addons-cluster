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
            this.modal = _(options).has('modal') ? options.modal : true;
        },
        start: function(){
            this.set_position();
        },
        renderElement: function(){
            this._super();
            this.$("a.close").off('click').click(_.bind(this.closePopup,this));
            $(window).unbind();
            $(window).bind('resize',this.set_position);
            if (this.draggable)
                this.$('.popup').draggable();
            if (this.modal){
                this.$el.addClass('modal_dialog');
            }
            this.set_position();
        },
        set_position: function(){
            this.$('.popup').position({my:"center",of:".point-of-sale"});
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

    module.Confirm = module.BasePopup.extend({
        template:'Confirm',
        init: function(parent,options){
            this._super(parent,options);
            this.title = options.title || "";
            this.msg = options.msg || "";
        },
        renderElement:function(){
            this._super();
            this.$('button[name=yes]').off('click').click(_.bind(this.onClickBtnYes,this));
            this.$('button[name=no]').off('click').click(_.bind(this.onClickBtnNo,this)); 
            this.$('button[name=yes]').focus();      
        },
        onClickBtnYes: function(){
            this.close();
            this.hide();
            this.trigger('yes');
        },
        onClickBtnNo: function(){
            this.close();
            this.hide();
            this.trigger('no');
        },
       
    })

}