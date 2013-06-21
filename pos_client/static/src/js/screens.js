function openerp_pos_screens_ex(instance,module){
    module.CustomerPopupWidget = module.PopUpWidget.extend({
        template:'CustomerPopupWidget',              
        show: function(){
            self = this;
            this._super(); 
            this.client = new instance.web.Model('res.partner');
            this.seniat_url = new instance.web.Model('seniat.url');
            this.build_form()         
        },
        build_form: function(){
            self = this;
            $("#customer-form").dialog({
                modal: true,
                width:600,
                height:650,
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
            $("#choice_type").change(_.bind(this.on_choice_type_change,this))
             
            $("#choice_taxpayer").buttonset();
            $("#choice_special_taxpayer").buttonset();
        },
        on_choice_type_change:function(e){
            type = $("#choice_type :radio:checked").val()
            $("#txt_vat").val(type)
        },
        on_btnsearch_click: function(){
            vat = $("#txt_vat").val()
            this.seniat_url.call('check_rif',[vat]).then(function(res){
                $("#txt_name").val(res.name)
            })
        }
        
    })
}

