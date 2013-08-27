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
            model.call('validate',[this.name,this.password],null).done(function(id){
                if (id){
                    self.trigger('algo',true)
                }else{
                    self.$el.effect('shake',function(){
                        alert = new module.Alert(self,{draggable:false,title:'Error',msg:'Wrong user or password'});
                        alert.appendTo($('.point-of-sale'));
                        alert.on('continue',self,self.onClickBtnCancel);
                    });                    
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
}