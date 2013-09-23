function pos_client_widgets(instance, module){
    module.PosWidget.include({
        build_widgets: function(){
            this._super();
            var self = this;   
            
            this.customer_form = new module.CustomerForm(this, {draggable:false});
            this.customer_form.appendTo($('.point-of-sale'));
            this.screen_selector.add_popup('customer-form',this.customer_form)

            this.select_customer_button = new module.HeaderButtonWidget(this,{
                label:'Customer',
                action: function(){self.screen_selector.show_popup('customer-form');},
            });
            this.select_customer_button.appendTo(this.$('#rightheader'));            
        }
    })
}

