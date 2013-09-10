function cash_count_widgets(instance, module){
    _t = instance.web._t;
    
    var _start =  module.PosWidget.prototype.start;
    module.PosWidget.include({
        start: function(){  
            var self = this
            return self.pos.ready.done(function(){
                instance.web.unblockUI();
                login_widget = new module.LoginWidget(this, {closeable:false,draggable:false});
                login_widget.appendTo($('.point-of-sale'));
                login_widget.on('auth',this,function(cashier){
                    self.pos.set('current_cashier',cashier)
                    instance.web.blockUI();
                    _start.call(self);
                });    
            });                
        },
        build_widgets: function(){
            this._super();  

            this.x_report_screen = new module.XReportScreen(this,{});
            this.x_report_screen.appendTo($('#rightpane'));
            this.screen_selector.add_screen('xreport',this.x_report_screen);

            this.login_widget = new module.LoginWidget(this, {closeable:false});
            this.login_widget.appendTo($('.point-of-sale'));            
            this.screen_selector.add_popup('login-widget',this.login_widget);
            
            this.close_widget = new module.CloseWidget(this, {closeable:false,draggable:false});
            this.close_widget.appendTo($('.point-of-sale'));            
            this.screen_selector.add_popup('close-widget',this.close_widget);

            _(this.close_button).extend({action:this.onClickBtnClose});
        },
        onClickBtnClose: function(){
            this.pos_widget.screen_selector.show_popup('close-widget');
        },
    });

    module.UsernameWidget.include({
        get_name: function(){
            name = this._super();
            return name + " - " + this.pos.get('current_cashier').name
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
    
    // ------------------------- X Report Widgets -----------------------------
    module.XReportInstrumentWidget = module.PosBaseWidget.extend({
        template:"XReportInstrumentWidget",
        init: function(parent, options){
            this._super(parent, options);
            this.bindInstrumentLineEvents();
            this.pos.bind('change:currentXReport',this.clear,this);
            this.instrumentLineWidgets = new Array();
        },
        start:function(){
            this.set_numpad_state(this.pos_widget.numpad.state);
        },
        renderElement: function() {
            this._super();
            var self = this

            for (var i=0;i<this.instrumentLineWidgets.length;i++){
                this.instrumentLineWidgets[i].destroy();
            }

            var position = this.scrollbar ? this.scrollbar.get_position() : 0;
            this.scrollbar = new module.ScrollbarWidget(this,{
                target_widget:   this,
                target_selector: '.instrument-scroller',
                name: 'instrument',
                track_bottom: true,
                on_show: function(){
                    self.$('.instrument-scroller').css({'width':'89%'},100);
                },
                on_hide: function(){
                    self.$('.instrument-scroller').css({'width':'100%'},100);
                },
            });

            this.scrollbar.replace(this.$('.placeholder-ScrollbarWidget'));
            this.scrollbar.set_position(position);
            this.updateTotal();
        },

        addLine: function(line){
            instrument_line = new module.XReportInstrumentLineWidget(this,{line:line});
            instrument_line.appendTo(this.$('#paymentlines'));
            instrument_line.on('selected',this,this.update_numpad);
            this.instrumentLineWidgets.push(instrument_line);
            this.scrollbar.auto_hide();
            instrument_line.focus();
        },
        clear: function(){
            this.currentXReportLines.unbind();
            this.bindInstrumentLineEvents();
            this.renderElement();
        },
        updateTotal: function(){
            var total = this.pos.get('currentXReport').getTotal();
            this.$('#payment-due-total').html(this.format_currency(total));
        },
        bindInstrumentLineEvents: function(){
            this.currentXReportLines =  this.pos.get('currentXReport').get('lines');
            this.currentXReportLines.bind('add',this.addLine,this);
            this.currentXReportLines.bind('all',this.updateTotal,this);
        },        
        update_numpad: function() {
            if (this.numpadState)
                this.numpadState.reset();
        },
        set_numpad_state: function(numpadState) {
            if (this.numpadState) {
                this.numpadState.unbind('set_value', this.set_value);
                this.numpadState.unbind('change:mode', this.setNumpadMode);
            }
            this.numpadState = numpadState;
            if (this.numpadState) {
                this.numpadState.bind('set_value', this.set_value, this);
                this.numpadState.bind('change:mode', this.setNumpadMode, this);
                this.numpadState.reset();
                this.setNumpadMode();
            }
        },
        setNumpadMode: function() {
            this.numpadState.set({mode: 'instrument'});
        },
        set_value: function(val) {
            instrument_line = this.pos.get('currentXReport').getSelectedLine();
            if (instrument_line)
                instrument_line.set_amount(val);
        },
        close: function(){
            this.currentXReportLines.unbind();
        },
    });

    module.XReportInstrumentLineWidget =  module.PosBaseWidget.extend({
        template:"XReportInstrumentLineWidget",
        events:{
            "click a.delete-payment-line":"onClickBtnDelete",
            "keyup input":"changeAmount",
            "click input":"focus",
        },
        init: function(parent, options){
            this._super(parent, options);
            this.line = options.line;
            this.line.bind('focus',this.focus,this);
            this.line.bind('change',this.changedAmount,this);
        },
        onClickBtnDelete: function(){
            this.pos.get('currentXReport').get('lines').remove(this.line);
            this.destroy();
        },
        changeAmount: function(e){
            var newAmount = e.currentTarget.value;
            var amount = parseFloat(newAmount);
            if(!isNaN(amount)){
                this.amount = amount;
                this.line.set('amount',amount);
            }
        },
        changedAmount: function() {
            if (this.amount !== this.line.get_amount()){
                this.renderElement();
            }
        },
        focus: function(){
            this.trigger('selected');
            this.pos.get('currentXReport').selectLine(this.line);
            var val = this.$('input')[0].value;
            this.$('input')[0].focus();
            this.$('input')[0].value = val;
            this.$('input')[0].select();
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