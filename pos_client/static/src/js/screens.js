function openerp_pos_screens_ex(instance,module){
    
    
    module.CustomerConfirm = module.PopUpWidget.extend({
        template:'CustomerConfirm',
        show: function(parent,msg){
            this.parent = parent;
            this.msg = msg;
            this._super();
            this.build_ui();
        },
        build_ui: function(){
            self = this;
            $("#customer-confirm #message").html(this.msg);
            $("#customer-confirm").dialog({
                modal: true,
                title: "Question",
                width:310,
                height:205,
                buttons:{
                    Yes:function(){
                        self.on_btnYes_click();
                        $(this).dialog('close');
                        self.close();
                    },
                    No:function(){
                        self.on_btnNo_click();
                        $(this).dialog('close');
                        self.close();
                    },
                                    
                }
            });
            
        },
        on_btnYes_click:function(){
        },
        on_btnNo_click:function(){
        },
        
    })
    
    
    module.CustomerConfirmUpdate = module.CustomerConfirm.extend({
        on_btnYes_click:function(){
            vat = $("#choiceType :radio:checked").val() + $("#txtVat").val();
            this.parent.seniat_request(vat);
            $("#txtStreet").focus();
        },
        on_btnNo_click:function(){
            $("#btnSave").focus();
        },
    })
    
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
            $("#customer-popup #message").html(this.msg);
            $("#customer-popup").dialog({
                modal: true,
                title: self.title,
                width:310,
                height:205,
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
                height:440,
                buttons:[
                    {
                        id:"btnSave",
                        text:"Save",
                        click:function(){
                            alert("we are the world");
                        }
                    },
                    {
                        text:"Cancel",
                        click:_.bind(self.on_btnCancel_click,this) 
                    },
                ],

            });
            $("#btnSearch").button({icons: {primary: "ui-icon-search"},text:false})          
            $("#choiceType").buttonset();             
            $("#choice_taxpayer").buttonset();
            $("#choice_special_taxpayer").buttonset();
            $("#txtVat").focus();           
        },
        customer_search: function(vat){
            var id = this.pos.db.search_customer(vat);
            return id;
        },
        ask_for_update:function(){
            ccu = new module.CustomerConfirmUpdate(this, {});
            ccu.appendTo($('.point-of-sale'));
            ccu.show(this,"This client already exists. Do you want to upgrade it?");
        },
        load_customer:function(id){
            customer = this.pos.db.get_customer_by_id(id);
            this.load_data(customer);
            this.ask_for_update();
            
        },
        load_data:function(c){            
            c.street = _.has(c,"street") ? c.street:""
            c.street2 = _.has(c,"street2") ? c.street2:""
            c.city = _.has(c,"city") ? c.city:""
            c.phone = _.has(c,"phone") ? c.phone:""
            c.email = _.has(c,"email") ? c.email:""
            $("#txtName").val(c.name);
            $("#txtStreet").val(c.street ? c.street:"");
            $("#txtStreet2").val(c.street2 ? c.street2:"");
            $("#txtCity").val(c.city ? c.city:"");
            $("#txtPhone").val(c.phone ? c.phone:"");
            $("#txtEmail").val(c.email ? c.email:"");
        },
        load_data_seniat:function(c){            
            $("#txtName").val(c.name);
            $("#chkSt").attr("checked",c.vat_subjected);
            $("#chkWh").attr("checked",c.wh_iva_agent);            
        },
        seniat_request:function(vat){
            self = this
            this.seniat_url.call('check_rif',[vat]).then(function(customer){
                if (customer != null){
                    self.load_data_seniat(customer);
                    self.enable_controls();
                    $("#txtStreet").focus();
                }
            }).fail(function(obj, event){ 
                alert("algo fallo");             
            })
        },
        on_btnSearch_click: function(){
            self = this;
            vat = $("#choiceType :radio:checked").val() + $("#txtVat").val();
            regex = new RegExp(/^[VEGJP]?([0-9]){1,9}(-[0-9])?$/);
            if (regex.test(vat)){
                id = this.customer_search(vat)
                if (id != -1)
                    this.load_customer(id);
                else
                    this.seniat_request(vat);
            }else{
                self.show_popup("Error","This VAT number does not seem to be valid!");
            }

            
        },     
        show_popup: function(title,msg){
            customer_popup = new module.CustomerPopup(this, {});
            customer_popup.appendTo($('.point-of-sale'));
            customer_popup.show(title,msg);
        },
        clear:function(){
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
        on_btnCancel_click: function(){
            this.clear();
            this.disable_controls();
            $("#txtVat").focus();
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
            $("#chkSt").removeAttr("disabled");
            $("#chkWh").removeAttr("disabled");
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

