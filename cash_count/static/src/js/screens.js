function cash_count_screens(instance, module){

    module.LoginScreen = module.ScreenWidget.extend({
        template: 'LoginScreen',
        next_screen: 'products',
        show_numpad:     false,
        show_leftpane:   false,

        show: function(){
            this._super();
            var self = this;
            this.pos_widget.set_cashier_controls_visible(false);

            this.add_action_button({
                label: _t('Exit'),
                icon: '/point_of_sale/static/src/img/icons/png48/system-log-out.png',
                click: function(){  
                    self.pos_widget.try_close();                     
                }
            });

            this.add_action_button({
                label: _t('Unlock'),
                icon: '/cash_count/static/src/img/unlock.png',
                click: function(){
                    var msg = "This action requires manager credentials. Do you want to continue?"
                    confirm = new module.Confirm(this,{title:"Confirm",msg:msg});
                    confirm.appendTo($('.point-of-sale'));
                    confirm.show();
                    confirm.on('yes',this,function(){
                        self.pos_widget.screen_selector.show_popup('manager-widget');
                    });
                }
            });
            setTimeout(this.proxy('showPopup'), 500);
        },
        showPopup: function(){
            this.login_widget = new module.LoginWidget(this, {modal:false,closeable:false,draggable:false});
            this.login_widget.appendTo($('.point-of-sale'));
            this.login_widget.show();

        },
    });

    module.OpeningScreen = module.ScreenWidget.extend({
        template: 'OpeningScreen',
        back_screen: 'login-screen',
        next_screen: 'products', 
        show_numpad:     false,
        show_leftpane:   false,
        show: function(){
            this._super();
            var self = this;
            this.pos_widget.set_cashier_controls_visible(false);
            this.opening_widget = new module.OpeningWidget(this, {modal:false,closeable:false,draggable:false});
            this.opening_widget.appendTo($('.point-of-sale'));

            this.add_action_button({
                label: _t('Back'),
                icon: '/point_of_sale/static/src/img/icons/png48/go-previous.png',
                click: function(){
                    self.pos.set('current_cashier',null);
                    self.close(); 
                    self.pos_widget.screen_selector.set_current_screen(self.back_screen);
                    
                }
            });
        },
        close: function(){
            this._super();
            if (this.opening_widget){
                this.opening_widget.hide();
                this.opening_widget.close();
            }
        },
    });

    module.XReportScreen = module.ScreenWidget.extend({
        template:'XReportScreen',
        back_screen: 'products',
        init: function(parent, options){
            this._super(parent, options); 
        },
        show: function(){
            this._super();
            this.pos.new_x_report(); 
            this.build_ui();            
        },
        build_ui: function(){
            var self = this;
            this.pos_widget.set_cashier_controls_visible(false);
            this.pos_widget.set_leftpane_visible(true);
            this.paypad = new module.PaypadWidgetXReport(this, {});
            this.paypad.replace($('#paypad'));
            this.order_widget = new module.OrderWidgetXReport(this, {});
            this.order_widget.replace($('.order-container'));
            this.instrument_widget = new module.XReportInstrumentWidget(this,{});
            this.instrument_widget.replace($('.XReportInstrumentWidget-placeholder'));
            this.add_action_button({
                label: _t('Back'),
                icon: '/point_of_sale/static/src/img/icons/png48/go-previous.png',
                click: function(){  
                     self.pos_widget.screen_selector.set_current_screen(self.back_screen);
                     self.close();
                }
            });
            this.add_action_button({
                label: _t('Validate'),
                icon: '/point_of_sale/static/src/img/icons/png48/validate.png',
                click: function(){
                    self.validate();
                },
            });            
        },
        validate:function(){
            //need insert printer command here
            printer_serial = '1234';
            report_number = '001';
            this.pos.get('currentXReport').set('printer_serial',printer_serial);
            this.pos.get('currentXReport').set('report_number',report_number);
            this.pos.save_x_report();
         
        },
        close: function(){
            this._super();
            this.paypad = new module.PaypadWidget(this, {});
            this.paypad.replace($('#paypad'));
            this.order_widget = new module.OrderWidget(this, {});
            this.order_widget.replace($('.order-container'));
            this.instrument_widget.close();

        },
    });
}