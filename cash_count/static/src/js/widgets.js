function cash_count_widgets(instance, module){
    module.PosWidget.include({
        start: function(){  
            var self = this    
            pos = this._super()           
            return self.pos.ready.done(function() {
                alert("identify_cashier");
            })
        },
    })
}