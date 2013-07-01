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
                height:210,
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
            $("#btnSave span").text("Save");
            $("#txtStreet").focus();
        },
        on_btnNo_click:function(){
            $("#btnSave span").text("Accept");
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
                        $("#txtVat").focus();
                        $(this).dialog('close');
                        self.close();
                    }                
                }
            });
            
        }
    })
        
    module.CustomerPopupForm = module.PopUpWidget.extend({
        template:'CustomerPopupForm',
        events:{
            "click button[name='cancel']":"onClickBtnCancel",
            "click button[name='search']":"onClickBtnSearch",
            "change .oe_text_field": "onChangeTextbox",
            "change input[type='radio']":"onChangeRadio",
            "change input[name='vat_subjected']":"onChangeVatSubjected",
            "change input[name='wh_iva_agent']":"onChangeWhIvaAgent",  
            "keypress input[name='vat']":"onKeypressVat", 
            "keypress input[name='street']":"onKeypressStreet",
            "keypress input[name='street2']":"onKeypressStreet2",
            "keypress input[name='city']":"onKeypressCity",
            "keypress input[name='phone']":"onKeypressPhone", 
            "keypress input[name='email']":"onKeypressEmail",                
        },       
        init: function(parent, options){
            this._super(parent, options);
            this.customer = new module.Customer();
            this.customer.bind('change',this.renderElement,this)
            this.letter = "V";
            
        }, 
        show: function(){
            self = this;
            this._super(); 
            this.ready = $.Deferred();
            this.seniat_url = new instance.web.Model('seniat.url');
            this.build_form();
            this.disable_controls();
            $("#txtVat").focus(); 
            
    
        },        
        build_form: function(){
            self = this;             
            $("#choiceType").buttonset();                     
        },
        customer_search: function(vat){
            var id = this.pos.db.search_customer(vat);
            return id;
        },
        ask_for_update:function(){
            ccu = new module.CustomerConfirmUpdate(this, {});
            ccu.appendTo($('.point-of-sale'));
            ccu.show(this,"This client already exists. Do you want to upgrade it?");
            $("#btnSave span").text("Accept");
            
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
            letter = $("#choiceType :radio:checked").val();
            $("#txtName").val(c.name);
            $("#chkWh").attr("checked",c.wh_iva_agent);         
            $("#chkWh").attr("checked",c.wh_iva_agent);         
            if (letter != "V")
                $("#chkSt").attr("checked",c.vat_subjected);
                        
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
        save_customer: function(){
            alert(this.customer.get('street'));
        },
        onClickBtnSave:function(){
           console.debug(this.customer);
           text = $("#btnSave span").text();   
           if (text == "Save")
                this.save_customer();
           else
                alert("select")
        },         
        show_popup: function(title,msg){
            customer_popup = new module.CustomerPopup(this, {});
            customer_popup.appendTo($('.point-of-sale'));
            customer_popup.show(title,msg);
        },    
        disable_controls : function(){
            this.$("#txtVat").removeAttr("disabled");
            this.$("#btnSearch").removeAttr("disabled","disabled");            
            this.$("input[name='name']").attr("disabled","disabled");
            this.$("#txtStreet").attr("disabled","disabled");
            this.$("#txtStreet2").attr("disabled","disabled");
            this.$("#txtCity").attr("disabled","disabled");
            this.$("#txtPhone").attr("disabled","disabled");
            this.$("#txtEmail").attr("disabled","disabled");
            this.$("#chkSt").attr("disabled","disabled");
            this.$("#chkWh").attr("disabled","disabled");
            this.$("#choiceType :radio").button("enable");
        },
        enable_controls : function(){          
            this.$("#txtStreet").removeAttr("disabled");
            this.$("#txtStreet2").removeAttr("disabled");
            this.$("#txtCity").removeAttr("disabled");
            this.$("#txtPhone").removeAttr("disabled");
            this.$("#txtEmail").removeAttr("disabled");
            this.$("#chkSt").removeAttr("disabled");
            this.$("#chkWh").removeAttr("disabled");
            this.$("#txtVat").attr("disabled","disabled");
            this.$("#btnSearch").attr("disabled","disabled");
            this.$("#choiceType :radio").button("disable");         
        },
        renderElement: function(){
            ids = $('input:disabled')
            this._super();
            this.build_form();
            $(ids).each(function(index,value){
                console.debug(value.name) 
                $("input[name='"+value.name+"']").attr("disabled","disabled");               
            });
        },
        clear:function(){
            this.customer.clear().set(this.customer.defaults);
        },   
        onClickBtnSearch: function(){            
            vat = this.letter + this.$("input[name='vat']").val();
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
         onClickBtnCancel: function(){
            this.clear();
            this.disable_controls();
            $("#txtVat").focus();
        },    
        onChangeTextbox:function(e){
            name = e.target.name;
            value = e.target.value;
            this.customer.set(name,value);
        },
        onChangeRadio:function(e){
            this.letter = e.target.value;
            this.$("#txtVat").focus();
        },
        onChangeVatSubjected:function(e){
            this.set('vat_subjected',e.target.value);
        },
        onChangeWhIvaAgent:function(e){
            this.set('wh_iva_agent',e.target.value)
        },  
        onKeypressVat:function(e){
            if (e.which == '13'){
                this.customer.set('vat',e.target.value);
                this.$("#btnSearch").trigger('click');
                e.preventDefault();
            }
        },
        onKeypressStreet:function(e){            
            if (e.which == '13'){
                this.$("#txtStreet2").focus();
                e.preventDefault();
            }
        }, 
        onKeypressStreet2:function(e){            
            if (e.which == '13'){
                this.$("#txtCity").focus();
                e.preventDefault();
            }
        }, 
        onKeypressCity:function(e){            
            if (e.which == '13'){
                this.$("#txtPhone").focus();
                e.preventDefault();
            }
        },
        onKeypressPhone:function(e){            
            if (e.which == '13'){
                this.$("#txtEmail").focus();
                e.preventDefault();
            }
        },
        onKeypressEmail:function(e){            
            if (e.which == '13'){
                this.$("#btnSave").focus();
                e.preventDefault();
            }
        },
        
        
    })
}

