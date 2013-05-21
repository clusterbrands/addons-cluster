function openerp_pos_widgets_ex(instance, module){ 
    
    //realizar comprobaciones aqui
    module.PosWidget.include({
        start: function(){  
            var self = this          
            pos = this._super()
            return self.pos.ready.done(function() {
                console.debug("estoy aqui")
                if (self.pos.get('pos_config').printer == null)
                    self.screen_selector.show_popup('not-printer-error');
                else
                    console.debug("proxy: "+self.pos.proxy)
            })
        }
    })
    
    //@overwritten
    module.PosWidget.include({
        build_widgets: function(){
            this._super()
            var self = this;
            
            this.select_customer_popup = new module.SelectCustomerPopupWidget(this, {});
            this.select_customer_popup.appendTo($('.point-of-sale'));
            
            this.not_printer_error_popup = new module.NotPrinterErrorPopupWidget(this,{})
            this.not_printer_error_popup.appendTo($('.point-of-sale'));
            
            this.select_customer_button = new module.HeaderButtonWidget(this,{
                label:'Select Customer',
                action: function(){ self.screen_selector.show_popup('select-customer'); },
            });
            this.select_customer_button.appendTo(this.$('#rightheader'));

            this.customername = new module.CustomernameWidget(this,{});
            this.customername.appendTo(this.$('#rightheader'));
        
            this.screen_selector = new module.ScreenSelector({
                pos: this.pos,
                screen_set:{
                    'products': this.product_screen,
                    'payment' : this.payment_screen,
                    'client_payment' : this.client_payment_screen,
                    'scale_invite' : this.scale_invite_screen,
                    'scale':    this.scale_screen,
                    'receipt' : this.receipt_screen,
                    'welcome' : this.welcome_screen,
                },
                popup_set:{
                    'help': this.help_popup,
                    'error': this.error_popup,
                    'error-product': this.error_product_popup,
                    'error-session': this.error_session_popup,
                    'error-negative-price': this.error_negative_price_popup,
                    'choose-receipt': this.choose_receipt_popup,
                    'select-customer': this.select_customer_popup,
                    'not-printer-error':this.not_printer_error_popup,
                },
                default_client_screen: 'welcome',
                default_cashier_screen: 'products',
                default_mode: this.pos.iface_self_checkout ?  'client' : 'cashier',
            });

          
        }
    })
    
    module.CustomernameWidget = module.PosBaseWidget.extend({
        template: 'CustomernameWidget',
        init: function(parent, options){
            var options = options || {};
            this._super(parent,options);
            this.pos.bind('change:selectedOrder', this.renderElement, this);
        },
        refresh: function(){
            this.renderElement();
        },
        get_name: function(){
            var user;
            customer = this.pos.get('selectedOrder').get_client();
            if(customer){
                return customer.name;
            }else{
                return "";
            }
        },
    });
    
    module.CustomerWidget = module.PosBaseWidget.extend({
        template: 'CustomerWidget',
        init: function(parent, options) {
            this._super(parent,options);
            this.model = options.model;
            this.click_customer_action = options.click_customer_action;
        },
        renderElement: function() {
            this._super();
            var self = this;
            $("a", this.$el).click(function(e){
                if(self.click_customer_action){
                    self.click_customer_action(self.model.toJSON());
                }
            });
        },
    });
    
    module.CustomerListWidget = module.ScreenWidget.extend({
        template:'CustomerListWidget',
        init: function(parent, options) {
            var self = this;
            this._super(parent,options);
            this.model = options.model;
            this.customer_list = [];
            this.next_screen = options.next_screen || false;
            this.click_customer_action = options.click_customer_action;

            var customers = self.pos.db.get_all_customers();
            self.pos.get('customers').reset(customers);
            this.pos.get('customers').bind('reset', function(){
                self.renderElement();
            });
        },
        renderElement: function() {
            var self = this;
            this._super();
            this.customer_list = [];
             
            this.pos.get('customers')
                .chain()
                .map(function(customer) {
                    var customer = new module.CustomerWidget(self, {
                            model: customer,
                            next_screen: 'products',
                            click_customer_action: self.click_customer_action,
                    })
                    self.customer_list.push(customer);
                    return customer;
                })
                .invoke('appendTo', this.$('.customer-list'));

        },
    });
    
    module.NotPrinterErrorPopupWidget = module.ErrorPopupWidget.extend({
        template:'NotPrinterErrorPopupWidget',
        show: function(){
            self = this
            this._super();
            this.$('.button').off('click').click(function(){
                self.pos_widget.try_close()
            })
        }
        
    });
}
