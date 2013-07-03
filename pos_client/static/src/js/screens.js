function openerp_pos_screens_ex(instance,module){
    
    
    module.CustomerBasePopup = module.PopUpWidget.extend({
        template:"CustomerBasePopup",
        renderElement:function(){
            this._super();
            this.$("a.close").off('click').click(_.bind(this.closePopup,this))
        },
        closePopup:function(e){
            this.close();
            this.hide();
        },       
        
    });
    
    module.CustomerConfirm = module.CustomerBasePopup.extend({
        template:'CustomerConfirm',
        events:{
            "click button[name='confirm']":"onClickBtnConfirm",
            "click button[name='reject']":"onClickBtnReject",            
        },
        init: function(parent, options){
            this.id="customer-confirm";
            this._super();            
        },
        show: function(parent,title,msg){
            this.parent = parent;
            this.title = title;
            this.msg = msg;
            this._super();
            this.renderElement();
            this.build_ui();
        },
        build_ui:function(){
            this.$("#customer-confirm").position({my:"center",of:"#customer-form"});
            this.$(".popup").draggable();
        },
        onClickBtnConfirm:function(){
        },
        onClickBtnReject:function(){
        },
    })
    
    module.CustomerPopup = module.CustomerBasePopup.extend({
        template:'CustomerAlert',
        events:{
            "click button":function(e){
                this.close();
                this.hide();
            },            
        },
        init: function(parent, options){
            this.id="customer-alert";
            this._super();            
        },        
        show: function(title,msg){
            self = this;
            this.title = title;
            this.msg = msg;
            this._super();            
            this.renderElement();
            this.build_ui();           
        },
        build_ui:function(){
            this.$("#customer-alert").position({my:"center",of:"#customer-form"});
            this.$(".popup").draggable();
            this.$("button").focus();
        }
    });
    
    module.CustomerConfirmUpdate = module.CustomerConfirm.extend({
        show:function(parent,title,msg){
            this.renderElement();            
            this._super(parent,title,msg);
            this.$("button[name='reject']").focus();            
        },
        onClickBtnConfirm:function(){
            vat = this.parent.letter + this.parent.customer.get('vat');
            this.parent.seniat_request(vat);
            this.parent.setOperation("Update");
            this.parent.$("input[name='street']").focus();
            this.close();
            this.hide();
        },
        onClickBtnReject:function(){
            this.close();
            this.hide();
            this.parent.setOperation("Select");
            this.parent.$("button[name='save']").focus()
        },
    });
        
    module.CustomerForm = module.CustomerBasePopup.extend({
        template:'CustomerForm',
        events:{
            "click button[name='save']":"onClickBtnSave",
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
            this.id = "customer-form";
            this.customer = new module.Customer();
            this.letter = "V";
            this.operation="Create";
        }, 
        show: function(){
            self = this;
            this._super(); 
            this.ready = $.Deferred();
            this.seniat_url = new instance.web.Model('seniat.url');
            this.build_ui();
            this.disable_controls();
            $("#txtVat").focus();            
    
        },        
        build_ui: function(){
            self = this;             
            $("#choiceType").buttonset();           
            $("#customer-form").position({my:"center",of:".point-of-sale"});
            $(".popup").draggable();
        },
        renderElement: function(){
            ids = $('input:disabled')
            this._super();
            this.build_ui();
            $(ids).each(function(index,value){
                $("input[name='"+value.name+"']").attr("disabled","disabled");               
            });
        },
        setOperation:function(value){
            this.operation = value;
            this.renderElement();
        },
        clear:function(){
            this.operation = "Create";
            this.customer.clear().set(this.customer.defaults);
            this.renderElement();
        },
        customer_search: function(vat){
            var id = this.pos.db.search_customer(vat);
            return id;
        },
        ask_for_update:function(){
            ccu = new module.CustomerConfirmUpdate(this, {});
            ccu.appendTo($('.point-of-sale'));
            ccu.show(this,"Question","This customer already exists. Do you want to upgrade it?");          
        },
        load_customer:function(c){
            this.load_data(c);
            this.ask_for_update();
            
        },
        load_data:function(c){          
            this.customer.set('name',c.name || "");
            this.customer.set('vat_subjected',c.vat_subjected || null);
            this.customer.set('wh_iva_agent',c.wh_iva_agent || null);
            this.customer.set('street',c.street || "");
            this.customer.set('street2',c.street2 || "");
            this.customer.set('city',c.city || "");
            this.customer.set('phone',c.phone || "");
            this.customer.set('email',c.email || "");
            this.renderElement();
        },
        load_data_seniat:function(c){
            this.customer.set("name",c.name)          
            this.customer.set("wh_iva_agent",c.wh_iva_agent)
            if (this.letter != "V")
                this.customer.set("vat_subjected",c.vat_subjected);
            this.renderElement();
        },
        seniat_request:function(vat){
            self = this
            this.seniat_url.call('check_rif',[vat]).then(function(customer){
                if (customer != null){
                    self.load_data_seniat(customer);
                    self.enable_controls();
                    self.$("input[name='street']").focus();
                }
            }).fail(function(obj, event){ 
                alert("algo fallo");             
            })
        },
        save_customer: function(){
        },
        show_popup: function(title,msg){
            customer_popup = new module.CustomerPopup(this, {});
            customer_popup.appendTo($('.point-of-sale'));
            customer_popup.show(title,msg);
        },    
        disable_controls : function(){              
            this.$("input[type=text]").attr("disabled","disabled");
            this.$(":checkbox").attr("disabled","disabled");
            this.$("input[name='vat']").removeAttr("disabled");
            this.$("button[name='search']").removeAttr("disabled","disabled"); 
            this.$("#choiceType :radio").button("enable");                             
        },
        enable_controls : function(){          
            this.$("input[type=text]").removeAttr("disabled");
            this.$(":checkbox").removeAttr("disabled");
            this.$("input[name='vat']").attr("disabled","disabled");
            this.$("button[name='search']").attr("disabled","disabled");
            this.$("#choiceType :radio").button("disable");         
        },
        onClickBtnSave:function(){
           if (this.operation == "Create")
                this.save_customer();
            
        }, 
        onClickBtnSearch: function(){            
            vat = this.letter + this.customer.get('vat');
            regex = new RegExp(/^[VEGJP]?([0-9]){1,9}(-[0-9])?$/);
            if (regex.test(vat)){
                c = this.customer_search(vat)
                if (c != null)
                    this.load_customer(c);
                else
                    this.seniat_request(vat);
            }else{
                this.show_popup("Error","This VAT number does not seem to be valid!");
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
                this.$("button[name='save']").focus();
                e.preventDefault();
            }
        },
        
        
    })
}

