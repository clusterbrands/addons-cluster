function openerp_pos_screens_ex(instance,module){
    module.CustomerPopupWidget = module.PopUpWidget.extend({
        template:'CustomerPopupWidget',        
        start: function(){
            this._super();
            var self = this;
            console.debug("hola mundo")
        },        
        show: function(){
            this._super();
            var self = this;
            this.renderElement();
        },
    })
}

