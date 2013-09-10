function cash_count_screens(instance, module){

    module.LoginWidget = module.BasePopup.extend({
        template:"LoginWidget",
        events:{
            "click button[name='cancel']":"onClickBtnCancel",
            "click button[name='validate']":"onClickBtnValidate",
            "change input[name='name']": "onChangeTxtName",
            "change input[name='password']":"onChangeTxtPassword",
        },
        init: function(parent, options){
            this._super(parent, options);
            this.name = "";
            this.password = "";
        },
        start: function(){
            this._super();
            this.$("input[name='name']").focus();
        },
        onClickBtnCancel: function(){
            this.name = "";
            this.password = "";
            this.renderElement();
            this.$("input[name='name']").focus();
        },
        onClickBtnValidate:function(){
            var self = this;
            model = new instance.web.Model('cash.count.cashier');
            model.call('validate',[this.name,this.password],null).done(function(cashier){
                if (!_.isEmpty(cashier)){
                    self.trigger('auth',cashier)
                }else{                   
                    alert = new module.Alert(self,{draggable:false,title:'Error',msg:'Wrong user or password'});
                    alert.appendTo($('.point-of-sale'));
                    alert.on('continue',self,self.onClickBtnCancel);                                       
                }
            });
        },
        onChangeTxtName: function(e){
            this.name = e.target.value;
        },
        onChangeTxtPassword: function(e){
            this.password = e.target.value;
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