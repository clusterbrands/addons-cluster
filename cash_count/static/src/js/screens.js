function cash_count_screens(instance, module){
    var QWeb = instance.web.qweb;

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
            if (this.pos.get('cashier_session'))
                this.add_action_button({
                    label: _t('Unlock'),
                    icon: '/cash_count/static/src/img/unlock.png',
                    click: function(){
                        var msg = "This action requires manager credentials. Do you want to continue?"
                        confirm = new module.Confirm(this,{title:"Confirm",msg:msg});
                        confirm.appendTo($('.point-of-sale'));
                        confirm.show();
                        confirm.on('yes',this,function(){
                            manager_widget = new module.ManagerLoginWidget(self, {draggable:false});
                            manager_widget.appendTo($('.point-of-sale'));
                            manager_widget.show();
                        });
                    }
                });
            setTimeout(this.proxy('showPopup'), 300);
        },
        showPopup: function(){
            this.pos_widget.screen_selector.show_popup('login-widget');
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
        next_screen: 'xreport-receipt',

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
            this.pos.save_x_report();
            // var self = this
            // var model = new instance.web.Model('cash.count.cashier.session');
            // var session_id = self.pos.get('cashier_session').id
            // model.call('close_session',[session_id],null).done(function(response){
            //     self.pos_widget.screen_selector.set_current_screen(self.next_screen);
            // });
           
         
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

    module.XReportReceiptScreen = module.ScreenWidget.extend({
        template: 'XReportReceiptScreen',
        show_numpad:     false,
        show_leftpane:   false,

        init: function(parent, options) {
            this._super(parent,options);
            this.user = this.pos.get('user');
            this.company = this.pos.get('company');
            this.shop_obj = this.pos.get('shop');
            this.cashier = ""

        },

        renderElement: function() {
            this._super();
            this.pos.bind('change:currentXReport', this.changeCurrentReport, this);
        },

        changeCurrentReport: function() {
            if (this.currentXReportLines)
                this.currentXReportLines.unbind();
            this.currentXReportLines = (this.pos.get('currentXReport')).get('lines');
            this.currentXReportLines.bind('add', this.refresh, this);
            this.currentXReportLines.bind('change', this.refresh, this);
            this.currentXReportLines.bind('remove', this.refresh, this);
            this.refresh();
        },

        refresh: function() {
            this.currentXReport = this.pos.get('currentXReport');
            this.cashier = this.pos.get('cashier');
            this.$('.pos-receipt-container', this.$el).html(QWeb.render('XReportTicket',{widget:this}));
        },

        show: function(){
            this._super();
            var self = this;
            this.pos_widget.set_cashier_controls_visible(false);

            this.currentXReport = this.pos.get('currentXReport');
            this.currentXReportLines = this.currentXReport.get('lines').models

            this.add_action_button({
                label: _t('Print'),
                icon: '/point_of_sale/static/src/img/icons/png48/printer.png',
                click: function(){  
                    self.print();
                }
            });

            this.add_action_button({
                label: _t('Exit'),
                icon: '/point_of_sale/static/src/img/icons/png48/system-log-out.png',
                click: function(){
                    self.pos_widget.try_close();
                },
            });
            setTimeout(this.proxy('print'), 300);

        },
        print: function() {
            window.print();
        },
    });
}