function cash_count_widgets(instance, module){
    
    var _start =  module.PosWidget.prototype.start;
    module.PosWidget.include({
        start: function(){  
            var self = this
            return self.pos.ready.done(function(){
                instance.web.unblockUI();
                login_widget = new module.LoginWidget(this, {closeable:false,draggable:false});
                login_widget.appendTo($('.point-of-sale'));
                login_widget.on('algo',this,function(){
                     instance.web.blockUI();
                    _start.call(self);
                });    
            });                
        },
        build_widgets: function(){
            this._super();         
            this.login_widget = new module.LoginWidget(this, {closeable:false});
            this.login_widget.appendTo($('.point-of-sale'));            
            this.screen_selector.add_popup('login-widget',this.login_widget);
        },
    })

        
}