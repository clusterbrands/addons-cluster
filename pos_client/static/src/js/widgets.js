function openerp_pos_widgets_ex(instance, module){
    console.debug("module "+module)
    module.PosWidget.include({
        build_widgets: function(){
            this._super();
            var self = this;   
            
            this.customer_form = new module.CustomerForm(this, {});
            this.customer_form.appendTo($('.point-of-sale'));
            
            this.select_customer_button = new module.HeaderButtonWidget(this,{
                label:'Customer',
                action: function(){self.screen_selector.show_popup('customer-form');},
            });
            this.select_customer_button.appendTo(this.$('#rightheader'));
            
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
                    'customer-form': this.customer_form,
                },
                default_client_screen: 'welcome',
                default_cashier_screen: 'products',
                default_mode: this.pos.iface_self_checkout ?  'client' : 'cashier',
            });
        }
    })
}

