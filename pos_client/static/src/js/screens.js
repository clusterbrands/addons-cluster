function openerp_pos_screens_ex(instance,module){
    module.CustomerPopupWidget = module.PopUpWidget.extend({
        template:'CustomerPopupWidget',              
        show: function(){
            self = this;
            this._super();
            $("#customer-form").dialog({
                modal: true,
                width:600,
                height:600,
                buttons:{
                    Save:function(){
                    
                    },
                    Cancel:function(){
                        $(this).dialog("close");
                        self.pos_widget.screen_selector.close_popup()
                    }                
                }
            });
            $("#search").button({icons: {primary: "ui-icon-search"},text:false})
            $("#search").click(_.bind(this.on_btnsearch_click,this))
            $("#choice_type").buttonset();
            $("#choice_taxpayer").buttonset();
            $("#choice_special_taxpayer").buttonset();
        },
        on_btnsearch_click: function(){
            alert("Searching customer...")
        }
        
    })
}

