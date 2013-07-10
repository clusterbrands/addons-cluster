function openerp_pos_screens_ex(instance,module){
    
    module.PaymentScreenWidget.include({
        validateCurrentOrder : function(){
            currentOrder = this.pos.get('selectedOrder');
            if(currentOrder.get_client()!= null)
                this._super()
            else{
                popup = new module.CustomerAlert(this, {});
                popup.appendTo($('.point-of-sale'));
                popup.show("Error","Please select a customer    ");
                popup.set_position("center",".point-of-sale");
                
            }                
        }        
    })
    
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
            this._super(parent, options);            
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
            "click button":"onClickBtn",
        },
        init: function(parent, options){
            this.id="customer-alert";
            this._super(parent, options);            
        },        
        show: function(title,msg,el){
            self = this;
            this.title = title;
            this.msg = msg;
            this.elem = el;
            this._super();            
            this.renderElement();
            this.build_ui();           
        },
        build_ui:function(){
            this.$("#customer-alert").position({my:"center",of:"#customer-form"});
            this.$(".popup").draggable();
            this.$("button").focus();
        },
        set_position:function(position,parent){
            this.$("#customer-alert").position({my:position,of:parent});
        },
        onClickBtn: function(e){
            $(this.elem).focus();
            this.close();
            this.hide();   
        }
    });
    
    module.CustomerAlert = module.CustomerPopup.extend({
        onClickBtn: function(e){
            console.debug(this)
            this.pos_widget.screen_selector.show_popup('customer-form');
            this.close();
            this.hide();             
        }
    })
    
    module.CustomerConfirmUpdate = module.CustomerConfirm.extend({
        show:function(parent,title,msg){
            this.renderElement();            
            this._super(parent,title,msg);
            this.$("button[name='reject']").focus();            
        },
        onClickBtnConfirm:function(){
            vat = this.parent.customer.get('vat');
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
    
    module.CustomerConfirmContinue = module.CustomerConfirm.extend({
        show:function(parent,title,msg){
            this.renderElement();            
            this._super(parent,title,msg);
            this.$("button[name='reject']").focus();            
        },
        onClickBtnConfirm:function(){
            this.parent.enable_controls();
            this.parent.$("input[name='name']").focus();
            this.parent.customer.set('seniat_updated',false);
            this.close();
            this.hide();
        },
        onClickBtnReject:function(){
            this.close();
            this.hide();
            this.parent.$("input[name='vat']").focus();
        },
    });
        
    module.CustomerForm = module.CustomerBasePopup.extend({
        template:'CustomerForm',
        events:{
            "click button[name='save']":"onClickBtnSave",
            "click button[name='cancel']":"onClickBtnCancel",
            "click button[name='search']":"onClickBtnSearch",
            "change input[type='text']": "onChangeTextbox",
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
            this.operation = "Create"; 
        }, 
        show: function(){
            self = this;
            this._super(); 
            this.seniat_url = new instance.web.Model('seniat.url');
            this.build_ui();
            this.disable_controls();
            this.initialize()
            
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
        initialize:function(){
            this.operation = "Create";                  
            this.customer = new module.Customer();
            this.customer.setVatLetter(this.$(":radio:first").val()); 
            this.renderElement();
            this.$("input[name='vat']").focus()
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
            this.customer.set({
                'id':c.id,
                'name':c.name || "",
                'vat_subjected':c.vat_subjected,
                'wh_iva_agent':c.wh_iva_agent,
                'street':c.street || "",
                'street':c.street || "",
                'street2':c.street2 || "",
                'city':c.city || "",
                'phone':c.phone || "",
                'email':c.email || "",
            });                
            this.renderElement();
        },
        load_data_seniat:function(c){
            this.customer.set("seniat_updated",true);
            this.customer.set("name",c.name);          
            this.customer.set("wh_iva_agent",c.wh_iva_agent);
            if (this.customer.getVatLetter() != "V")
                this.customer.set("vat_subjected",c.vat_subjected);
            this.renderElement();
        },
        not_found_seniat:function(){
            ccc = new module.CustomerConfirmContinue(this, {});
            ccc.appendTo($('.point-of-sale'));
            ccc.show(this,"Question","This vat number is not found in SENIAT. Do you want to continue?");          
        },
        seniat_request:function(vat){
            self = this
            this.disable_buttons();
            this.seniat_url.call('check_rif',[vat]).then(function(customer){
                if (customer){
                    self.load_data_seniat(customer);
                    self.enable_controls();
                    self.$("input[name='street']").focus();
                } 
                self.enable_buttons();               
            }).fail(function(obj, event){ 
                event.preventDefault();
                ccc = new module.CustomerConfirmContinue(this, {});
                ccc.appendTo($('.point-of-sale'));
                ccc.show(self,"Connection error","Could not connect to SENIAT. Do you want to continue?"); 
                self.enable_buttons(); 
            })
        },
        validateFields:function(){
            if (this.customer.get('vat') == undefined){
                this.show_popup("Error","The field 'vat' is required","input[name='vat']");
                return false;
            }else if (this.customer.get('name')==undefined){
                this.show_popup("Error","The field 'name' is required","input[name='name']");
                return false;
            }else if (this.customer.get('street')==undefined){
                this.show_popup("Error","The field 'street' is required","input[name='street']");
                return false;
            }else if (this.customer.get('city')==undefined){
                this.show_popup("Error","The field 'city' is required","input[name='city']");
                return false;
            }else if (this.customer.get('phone')==undefined){
                this.show_popup("Error","The field 'phone' is required","input[name='phone']");
                return false;
            }
            return true;
        },
        saveCustomer:function(){
            if (this.operation == "Create")
                this.createCustomer();
            else if (this.operation == "Update")
                this.updateCustomer();
            else
                this.selectCustomer();
        },
        createCustomer:function(){    
            this.pos.create_customer(this.customer.toJSON()); 
            this.show_popup("Notification","Customer successfully created");
            this.selectCustomer();
        },
        updateCustomer:function(){
            if (this.customer.hasChanged()){
                c = this.customer.changedAttributes();
                c.id = this.customer.get('id');
                c.vat = this.customer.get('vat');
                console.debug(c);                 
                this.pos.update_customer(c);
                this.show_popup("Notification","Customer successfully update");           
            }
            this.selectCustomer();
        },
        selectCustomer:function(){
            this.pos.get('selectedOrder').set_client(this.customer.toJSON());
            this.pos.set('client',this.customer.toJSON());
            this.onClickBtnCancel()
            this.close();
            this.hide(); 
        },
        show_popup: function(title,msg,el){
            customer_popup = new module.CustomerPopup(this, {});
            customer_popup.appendTo($('.point-of-sale'));
            customer_popup.show(title,msg,el);
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
        enable_buttons:function(){
            this.$(":button").removeAttr("disabled");
        },
        disable_buttons:function(){
            this.$(":button").attr("disabled","disabled");
        },      
        onClickBtnSave:function(){
            if (this.validateFields())
                this.saveCustomer();
        }, 
        onClickBtnSearch: function(){
            vat = this.customer.get('vat');
            console.log(vat)
            regex = new RegExp(/^[A-Z]{2}[VE]?([0-9]){1,9}$|^[A-Z]{2}[JGP]?([0-9]){9}$/);
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
            this.initialize();
            this.disable_controls();
        },    
        onChangeTextbox:function(e){
            name = e.target.name;
            value = e.target.value;
            if (name != "vat")
                this.customer.set(name,value);
            else
                this.customer.setVatNumbers(value);
        },
        onChangeRadio:function(e){
            this.customer.setVatLetter(e.target.value);
            this.$("input[name='vat']").focus();;
        },
        onChangeVatSubjected:function(e){
            if (this.$(e.target).attr('checked'))
                this.customer.set('vat_subjected',true);
            else
                this.customer.set('vat_subjected',false);
        },  
        onChangeWhIvaAgent:function(e){
            if (this.$(e.target).attr('checked'))
                this.customer.set('wh_iva_agent',true)
            else
                this.customer.set('wh_iva_agent',false)
        },  
        onKeypressVat:function(e){
            if (e.which == '13'){
                this.customer.setVatNumbers(e.target.value);
                this.$("button[name='search']").trigger('click');
                e.preventDefault();
            }
        },
        onKeypressStreet:function(e){            
            if (e.which == '13'){
                this.$("input[name='street2']").focus();
                e.preventDefault();
            }
        }, 
        onKeypressStreet2:function(e){            
            if (e.which == '13'){
                this.$("input[name='city']").focus();
                e.preventDefault();
            }
        }, 
        onKeypressCity:function(e){            
            if (e.which == '13'){
                this.$("input[name='phone']").focus();
                e.preventDefault();
            }
        },
        onKeypressPhone:function(e){            
            if (e.which == '13'){
                this.$("input[name='email']").focus();
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

