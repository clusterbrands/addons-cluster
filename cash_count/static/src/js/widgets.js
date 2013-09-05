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
}