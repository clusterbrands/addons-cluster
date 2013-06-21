function openerp_pos_screens_ex(instance,module){
    module.CustomerPopupWidget = module.PopUpWidget.extend({
        template:'CustomerPopupWidget',              
        show: function(){
            self = this;
            this._super(); 
            this.client = new instance.web.Model('res.partner');
            this.seniat_url = new instance.web.Model('seniat.url');
            this.build_form();
            this.add_listeners();      
        },
        build_form: function(){
            self = this;
            $("#customer-form").dialog({
                modal: true,
                width:600,
                height:420,
                buttons:{
                    Save:function(){
                        $(this).icon({primary: "ui-icon-search"})
                    },
                    Cancel:function(){
                        $(this).dialog("close");
                        self.pos_widget.screen_selector.close_popup()
                    }                
                }
            });
            $("#search").button({icons: {primary: "ui-icon-search"},text:false})          
            $("#choice_type").buttonset();             
            $("#choice_taxpayer").buttonset();
            $("#choice_special_taxpayer").buttonset();
            $("#txtVat").focus()
        },
        add_listeners:function(){
            $("#search").click(_.bind(this.on_btnsearch_click,this));
            $("#txtVat").keypress(_.bind(this.on_txtVat_keypress,this));
            
        },
        on_txtVat_keypress:function(){
            
        },        
        on_btnsearch_click: function(){
            letter = $("#choice_type :radio:checked").val()
            vat = letter + $("#txt_vat").val() 
            this.seniat_url.call('check_rif',[vat]).then(function(res){
                $("#txt_name").val(res.name)
            })
        }
        
    })
}

