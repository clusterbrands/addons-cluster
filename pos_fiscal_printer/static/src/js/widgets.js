openerp.pos_fiscal_printer = function(instance){
    var module = instance.point_of_sale
    
    //@overwritten
    module.PosWidget.include({
        build_widgets: function(){
            this._super();      
            this.select_customer_popup = new module.SelectCustomerPopupWidget(this, {});
            this.select_customer_popup.appendTo($('.point-of-sale'));
            
            this.client_button = new module.HeaderButtonWidget(this,{
                label:'Self-Checkout',
                action: function(){ self.screen_selector.set_user_mode('client'); },
            });
            this.client_button.appendTo(this.$('#rightheader'));

            this.select_customer_button = new module.HeaderButtonWidget(this,{
                label:'Select Customer',
                action: function(){ self.screen_selector.show_popup('select-customer'); },
            });
            this.select_customer_button.appendTo(this.$('#rightheader'));
            
            this.screen_selector.popup_set['select-customer'] =  this.select_customer_popup     
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
}
