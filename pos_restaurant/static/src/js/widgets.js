function pos_restaurant_widgets(instance, module){
   
    module.ProductListWidget.include({
        init: function(parent, options){
            var self = this
            options.click_product_action = function(product){
                if(product.get('to_weight') && self.pos.iface_electronic_scale){
                    self.pos_widget.screen_selector.set_current_screen(self.scale_screen, {product: product});
                }else{
                    if (product.get('property_ids').length > 0)
                        self.show_selector(product)
                    else
                        self.pos.get('selectedOrder').addProduct(product);
                }
            },
            this._super(parent, options)
        },
        show_selector: function(product){
            property_selector = new module.PropertySelector(this,{product:product,draggable:false})
            property_selector.appendTo($('.point-of-sale'));
            property_selector.show();               
        },
    });

    module.PropertySelector = module.BasePopup.extend({
        template:'PropertySelector',
        events:{
            "click button[name='done']":"onClickBtnDone",
            "click button[name='next']":"onClickBtnNext",
            "click button[name='previous']":"onClickBtnPrevious",           
        },
        init: function(parent, options){
            var self = this
            this._super(parent, options)
            this.step = 0;
            this.product = options.product;
            this.product_properties = this.loadProperties(options.product);  
            this.current = this.product_properties.at(this.step);
            this.productwidgets = [];
            this.steps = this.product_properties.length;
            this.last = this.steps - 1;     
        },
        renderElement: function(){
            var self=this;
            this._super();

            for(var i = 0, len = this.productwidgets.length; i < len; i++){
                this.productwidgets[i].destroy();
            }
            this.productwidgets = []; 
            if(this.scrollbar){
                this.scrollbar.destroy();
            }
          
            _(this.current.get('optional_products')).each(function(p) {         
                var product = new module.CustomProductWidget(self, {
                    model: p,
                    click_product_action: self.click_product_action,
                });
                self.productwidgets.push(product);
                product.on('select',self,self.select);
                product.appendTo(self.$('.product-list'));                      
            });

            this.scrollbar = new module.ScrollbarWidget(this,{
                target_widget:   this,
                target_selector: '.product-list-scroller',
                on_show: function(){
                    self.$('.product-list-scroller').css({'padding-right':'62px'},100);
                },
                on_hide: function(){
                    self.$('.product-list-scroller').css({'padding-right':'0px'},100);
                },
            });

            this.scrollbar.replace(this.$('.placeholder-ScrollbarWidget'));

        },
        loadProperties : function(product){
            var self = this;
            var properties = new module.ProductPropertiesCollection();
            var product_properties = self.pos.get('product_properties');
            _(product.get('property_ids')).each(function(id) {
                var property = product_properties.get(id);
                var products = self.pos.get('products');
                var optional_products = []
                _.each(property.get('optional_product_ids'), function(p){
                    optional_products.push(products.get(p));
                });
                property.set('optional_products', optional_products);
                properties.push(property);
            });
            properties.sortByField('sequence')
            return properties
        },
        select: function(product, widget){
            if (this.current.get('single_choice')){
                _.each(this.productwidgets,function(w){
                    w.unSelect();
                });
            }
            widget.select();
        },
        set_step: function(value){
            this.step = value;
            this.current = this.product_properties.at(this.step);
            this.renderElement();
        },
        onClickBtnDone: function(){
            alert("Done");
        },
        onClickBtnPrevious: function(){
            if (this.product_properties.at(this.step - 1)){
                this.set_step(this.step - 1);
            }
        },
        onClickBtnNext: function(){
            if (this.product_properties.at(this.step + 1)){
                this.set_step(this.step + 1);
            }
        },
    });
    module.CustomProductWidget = module.ProductWidget.extend({
        init: function(parent, options) {
            this._super(parent,options);
            this.click_product_action = this.on_click_action;
        },
        on_click_action: function(){
            this.model.set('selected',!this.model.get('selected'));
            if (this.model.get('selected')){
                this.trigger('select', this.model, this);
            }else{
                this.$el.removeClass('selected');
            }
        },
        select:function(){
            this.model.set('selected', true);
            this.$el.addClass('selected');
        },
        unSelect: function(){ 
            this.model.set('selected', false);
            this.$el.removeClass('selected');
        },
        renderElement: function(){
            this._super();
            if (this.model.get('selected')){
                this.$el.addClass('selected');
            }
        },
    })
}