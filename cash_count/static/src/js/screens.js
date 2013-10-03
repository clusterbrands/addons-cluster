function cash_count_screens(instance, module){

    module.LoginWidget = module.BasePopup.extend({
        template:"LoginWidget",
        events:{
            "click button[name='clear']":"onClickBtnCancel",
            "click button[name='validate']":"onClickBtnValidate",
            "change input[name='user']": "onChangeTxtName",
            "change input[name='password']":"onChangeTxtPassword",
        },
        init: function(parent, options){
            this._super(parent, options);
            this.user = "";
            this.password = "";
        },
        start: function(){
            this._super();
            this.$("input[name='user']").focus();
        },
        onClickBtnCancel: function(){
            this.user = "";
            this.password = "";
            this.renderElement();
            this.$("input[name='user']").focus();
        },
        onClickBtnValidate:function(){
            var self = this;
            model = new instance.web.Model('hr.employee');
            model.call('login',[this.user,this.password],null).done(function(cashier){
                if (!_.isEmpty(cashier)){
                    self.pos.set('current_cashier',cashier)
                    self.pos_widget.screen_selector.set_current_screen('opening_screen');
                    self.hide();
                    self.close();
                }else{                   
                    alert = new module.Alert(self,{draggable:false,title:'Error',msg:'Wrong user or password'});
                    alert.appendTo($('.point-of-sale'));
                    alert.on('continue',self,self.onClickBtnCancel);                                       
                }
            });
        },
        onChangeTxtName: function(e){
            this.user = e.target.value;
        },
        onChangeTxtPassword: function(e){
            this.password = e.target.value;
        },
    });

    module.LoginScreen = module.ScreenWidget.extend({
        template: 'LoginScreen',
        next_screen: 'products',
        show_numpad:     false,
        show_leftpane:   false,

        show: function(){
            this._super();
            var self = this;
            this.pos_widget.set_cashier_controls_visible(false);

            login_widget = new module.LoginWidget(this, {modal:false,closeable:false,draggable:false});
            login_widget.appendTo($('.point-of-sale'));

            this.add_action_button({
                label: _t('Close'),
                icon: '/point_of_sale/static/src/img/icons/png48/system-log-out.png',
                click: function(){  
                    self.pos_widget.try_close();                     
                }
            });

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
                click: self.validate,
            });            
        },
        validate:function(){
        },
        close: function(){
            this._super();
            this.paypad = new module.PaypadWidget(this, {});
            this.paypad.replace($('#paypad'));
            this.order_widget = new module.OrderWidget(this, {});
            this.order_widget.replace($('.order-container'));
        },
    });
}