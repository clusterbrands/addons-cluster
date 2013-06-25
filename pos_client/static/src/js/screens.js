function openerp_pos_screens_ex(instance,module){
    
    module.CustomerPopup = module.PopUpWidget.extend({
        template:'CustomerPopup',
        show: function(title,msg){
            self = this;
            this.title = title;
            this.msg = msg;
            this._super();
            this.build_ui();
        },
        build_ui: function(){
            self = this;
            $("#message").html(this.msg);
            $("#customer-popup").dialog({
                modal: true,
                title: self.title,
                width:310,
                height:200,
                buttons:{
                    Ok:function(){
                        $(this).dialog('close');
                        self.close();
                    }                
                }
            });
            
        }
    })
        
    module.CustomerPopupForm = module.PopUpWidget.extend({
        template:'CustomerPopupForm',              
        show: function(){
            self = this;
            this._super(); 
            this.client = new instance.web.Model('res.partner');
            this.ready = $.Deferred();
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
        customer_search: function(){
            var self = this;
            var customers = this.pos.db.get_all_customers();
            console.debug(this.pos.db.customer_list_search_strings)
        },
        on_btnSearch_click: function(){
            self = this;
            vat = $("#choiceType :radio:checked").val() + $("#txtVat").val();
            regex = new RegExp(/^[VEGJP]?([0-9]){1,9}(-[0-9])?$/);
            if (regex.test(vat)){
                this.customer_search()
            }else{
                self.show_popup("Error","This VAT number does not seem to be valid!");
            }
            //~ this.seniat_url.call('check_rif',[vat]).then(function(res){
                //~ console.debug(res)
                //~ if (res !== null){
                    //~ $("#txtName").val(res.name);
                    //~ $("#chkSt").attr('checked',res.vat_subjected);
                    //~ $("#chkWh").attr('checked',res.wh_iva_agent);                    
                    //~ self.enable_controls();
                    //~ $("#txtStreet").focus();
                //~ }
            //~ }).fail(function(obj, event){
                //~ console.debug(obj)
                //~ if (obj.message == "XmlHttpRequestError"){
                    //~ alert("Error de Conexion");
                    //~ event.preventDefault();
                //~ }
            //~ })
            
        },     
        show_popup: function(title,msg){
            customer_popup = new module.CustomerPopup(this, {});
            customer_popup.appendTo($('.point-of-sale'));
            customer_popup.show(title,msg);
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
        add_listeners:function(){
            $("#btnSearch").off('click').click(_.bind(this.on_btnSearch_click,this));
            $("#choiceType").off('change').change(_.bind(this.on_choiceType_change,this));
            $("#txtVat").off('keypress').keypress(_.bind(this.on_txtVat_keypress,this));
            $("#txtStreet").off('keypress').keypress(_.bind(this.on_txtStreet_keypress,this));
            $("#txtStreet2").off('keypress').keypress(_.bind(this.on_txtStreet2_keypress,this));
            $("#txtCity").off('keypress').keypress(_.bind(this.on_txtCity_keypress,this));
            $("#txtPhone").off('keypress').keypress(_.bind(this.on_txtPhone_keypress,this));
            $("#txtEmail").off('keypress').keypress(_.bind(this.on_txtEmail_keypress,this));
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
        
        
    })
}

