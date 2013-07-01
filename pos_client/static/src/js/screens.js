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
        
    module.CustomerForm = module.CustomerBasePopup.extend({
        template:'CustomerForm',
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
            this.id = "customer-form";
            this.customer = new module.Customer();
            this.customer.bind('change',this.renderElement,this)
            parent= module.CustomerBasePopup
            this.events = _.extend({},parent.prototype.events,this.events)
            this.letter = "V";            
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
        customer_search: function(vat){
            var id = this.pos.db.search_customer(vat);
            return id;
        },
        ask_for_update:function(){
            ccu = new module.CustomerConfirm(this, {});
            ccu.appendTo($('.point-of-sale'));
            ccu.show(this,"Question","This customer already exists. Do you want to upgrade it?");
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
            this.build_ui();
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
                this.$("#btnSave").focus();
                e.preventDefault();
            }
        },
        
        
    })
}

