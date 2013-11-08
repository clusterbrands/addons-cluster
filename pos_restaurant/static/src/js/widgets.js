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
            property_selector = new module.PropertySelector(this,{product:product})
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
            var products = this.pos.get('products')
            _(this.current.get('optional_product_ids')).each(function(p) {
                if (products.get(p)){
                    var product = new module.CustomProductWidget(self, {
                        model: products.get(p),
                        click_product_action: self.click_product_action,
                    });
                    self.productwidgets.push(product);
                    product.on('select',self,self.select);
                    product.on('unselect',self,self.unSelect);
                    product.appendTo(self.$('.product-list'));     
                }              
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
                if (product_properties.get(id))
                    properties.push(product_properties.get(id));
            });
            properties.sortByField('sequence')
            return properties
        },
        select: function(product){
            console.debug(product)
            this.current.selected_products.push(product.id);
        },
        unSelect: function(product){
            
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
            console.debug(this.product_properties);
            if (this.product_properties.at(this.step + 1)){
                this.set_step(this.step + 1);
            }
        },
    });
    module.CustomProductWidget = module.ProductWidget.extend({
        init: function(parent, options) {
            this._super(parent,options);
            this.click_product_action = this.on_click_action;
            this.selected = false;
        },
        on_click_action: function(){
            this.selected = !this.selected;
            if (this.selected){
                this.$el.addClass('selected');
                this.trigger('select', this.model);
            }else{
                this.$el.removeClass('selected');
                this.trigger('unselect', this.model);
            }
        },
    })
}