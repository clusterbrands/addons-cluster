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
            this.disable_controls();      
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
                        console.debug(self)
                        self.on_btnCancel_click();
                        self.disable_controls();
                        $("#txtVat").focus();
                    }                
                }
            });
            $("#btnSearch").button({icons: {primary: "ui-icon-search"},text:false})          
            $("#choiceType").buttonset();             
            $("#choice_taxpayer").buttonset();
            $("#choice_special_taxpayer").buttonset();
            $("#txtVat").focus();
           
            
        },
        add_listeners:function(){
            $("#btnSearch").click(_.bind(this.on_btnSearch_click,this));
            $("#choiceType").change(_.bind(this.on_choiceType_change,this));
            $("#txtVat").keypress(_.bind(this.on_txtVat_keypress,this));
            $("#txtStreet").keypress(_.bind(this.on_txtStreet_keypress,this));
            $("#txtStreet2").keypress(_.bind(this.on_txtStreet2_keypress,this));
            $("#txtCity").keypress(_.bind(this.on_txtCity_keypress,this));
            $("#txtPhone").keypress(_.bind(this.on_txtPhone_keypress,this));
            $("#txtEmail").keypress(_.bind(this.on_txtEmail_keypress,this));
        },
        disable_controls : function(){
            $("#txtVat").removeAttr("disabled");
            $("#btnSearch").removeAttr("disabled","disabled");
            $("#choiceType :radio").button("enable");
            $("#txtName").attr("disabled","disabled");
            $("#txtStreet").attr("disabled","disabled");
            $("#txtStreet2").attr("disabled","disabled");
            $("#txtCity").attr("disabled","disabled");
            $("#txtPhone").attr("disabled","disabled");
            $("#txtEmail").attr("disabled","disabled");
            $("#chkSt").attr("disabled","disabled");
            $("#chkWh").attr("disabled","disabled");
        },
        enable_controls : function(){          
            $("#txtStreet").removeAttr("disabled");
            $("#txtStreet2").removeAttr("disabled");
            $("#txtCity").removeAttr("disabled");
            $("#txtPhone").removeAttr("disabled");
            $("#txtEmail").removeAttr("disabled");
            $("#txtVat").attr("disabled","disabled");
            $("#btnSearch").attr("disabled","disabled");
            $("#choiceType :radio").button("disable");
        },
        
        on_btnCancel_click: function(){
            $("#txtVat").val("");
            $("#txtName").val("");
            $("#txtStreet").val("");
            $("#txtStreet2").val("");
            $("#txtCity").val("");
            $("#txtPhone").val("");
            $("#txtEmail").val("");
            $("#chkSt").attr('checked',false);
            $("#chkWh").attr('checked',false);            
        },
        on_choiceType_change:function(){
            $("#txtVat").focus();
        },
        on_txtVat_keypress:function(e){            
            if (e.which == '13'){
                $("#btnSearch").trigger('click');
                e.preventDefault();
            }
        },
        on_txtStreet_keypress:function(e){            
            if (e.which == '13'){
                $("#txtStreet2").focus();
                e.preventDefault();
            }
        }, 
        on_txtStreet2_keypress:function(e){            
            if (e.which == '13'){
                $("#txtCity").focus();
                e.preventDefault();
            }
        }, 
        on_txtCity_keypress:function(e){            
            if (e.which == '13'){
                $("#txtPhone").focus();
                e.preventDefault();
            }
        },
        on_txtPhone_keypress:function(e){            
            if (e.which == '13'){
                $("#txtEmail").focus();
                e.preventDefault();
            }
        },
        on_txtEmail_keypress:function(e){            
            if (e.which == '13'){
                //
                e.preventDefault();
            }
        },
        on_btnSearch_click: function(){
            self = this;
            letter = $("#choiceType :radio:checked").val()
            vat = letter + $("#txtVat").val() 
            this.seniat_url.call('check_rif',[vat]).then(function(res){
                console.debug(res)
                if (res !== null){
                    $("#txtName").val(res.name);
                    $("#chkSt").attr('checked',res.vat_subjected);
                    $("#chkWh").attr('checked',res.wh_iva_agent);                    
                    self.enable_controls();
                    $("#txtStreet").focus();
                }
            })
        }
        
    })
}

