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

    module.CloseWidget =  module.BasePopup.extend({
        template:"CloseWidget",
        events:{
            "click button[name='cancel']":"onClickBtnCancel",
            "click button[name='reportx']":"onClickBtnReportX",
        },
        init: function(parent, options){
            this._super(parent, options);

        },
        onClickBtnCancel: function(){
            this.close();
            this.hide();
        },
        onClickBtnReportX: function(){
            this.pos_widget.screen_selector.set_current_screen('xreport');
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
            this.currentXReportLines =  this.pos.get('currentXReport').get('lines');
            this.currentXReportLines.bind('add',this.addReportLine,this);
            this.currentXReportLines.bind('all',this.updateTotal,this);
            this.updateTotal();
            this.build_ui();            
        },
        build_ui: function(){
            var self = this;
            this.pos_widget.set_cashier_controls_visible(false);
            this.paypad = new module.PaypadWidgetXReport(this, {});
            this.paypad.replace($('#paypad'));
            this.order_widget = new module.OrderWidgetXReport(this, {});
            this.order_widget.replace($('.order-container'));
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
                     self.pos_widget.screen_selector.set_current_screen(self.back_screen);
                     self.close();
                }
            });
        },
        close: function(){
            this._super();
            this.paypad = new module.PaypadWidget(this, {});
            this.paypad.replace($('#paypad'));
            this.order_widget = new module.OrderWidget(this, {});
            this.order_widget.replace($('.order-container'));
        },
        renderElement: function() {
            this._super();
            this.$('#paymentlines').empty();
        },
        updateTotal: function(){
            var total = this.pos.get('currentXReport').getTotal();
            this.$('#payment-due-total').html(this.format_currency(total));
        },
        addReportLine : function(line){
            var self = this
            line_widget = new module.XReportLineWidget(this,{line:line});
            line_widget.appendTo(this.$('#paymentlines'));
            line_widget.focus();
        },
    });

    module.PaypadWidgetXReport = module.PaypadWidget.extend({
        onInstrumentCashSelected: function(instrument){
            this.pos.get('currentXReport').addLine(instrument);
        },
        onInstrumentOtherSelected: function(instrument){
            this.pos.get('currentXReport').addLine(instrument);
        },
    })

    module.XReportLineWidget =  module.PosBaseWidget.extend({
        template:"XReportLineWidget",
        events:{
            "click a.delete-payment-line":"onClickBtnDelete",
            "keyup input":"changeAmount",
        },
        init: function(parent, options){
            this._super(parent, options);
            this.line = options.line;
        },
        onClickBtnDelete: function(){
            this.pos.get('currentXReport').get('lines').remove(this.line);
            this.destroy();
        },
        changeAmount: function(e){
            var newAmount = e.currentTarget.value;
            var amount = parseFloat(newAmount);
            if(!isNaN(amount)){
                this.line.set('amount',amount);
            }
        },
        focus: function(){
            var val = this.$('input')[0].value;
            this.$('input')[0].focus();
            this.$('input')[0].value = val;
            this.$('input')[0].select();
        },
    });

    module.OrderWidgetXReport = module.PosBaseWidget.extend({
        template:"OrderWidgetXReport",
        getCashierName: function(){
            return this.pos.get('currentXReport').get('cashier').name;
        },
        getUserName: function(){
            return this.pos.get('currentXReport').get('user').name;
        },
        getPosName: function(){
            return this.pos.get('currentXReport').get('pos_config').name;
        },
        getDate: function(){
            return this.pos.get('currentXReport').get('date');
        },
        getTime: function(){
            return this.pos.get('currentXReport').get('time');
        },
    })


}