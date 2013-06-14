function openerp_pos_widgets_ex(instance, module){
    console.debug("module "+module)
    module.PosWidget.include({
        build_widgets: function(){
            this._super();
            var self = this;            
            this.select_customer_button = new module.HeaderButtonWidget(this,{
                label:'Customer',
                action: function(){},
            });
            this.select_customer_button.appendTo(this.$('#rightheader'));
        }
    })
}

