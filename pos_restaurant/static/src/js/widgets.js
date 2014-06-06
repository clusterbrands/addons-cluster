function pos_restaurant_widgets(instance, module){
    
    module.ProductListWidget.include({
        init: function(parent, options){
            var self = this
            options.click_product_action = function(product){
                if(product.get('to_weight') && self.pos.iface_electronic_scale){
                    self.pos_widget.screen_selector.set_current_screen(self.scale_screen, {product: product});
                }else{
                    self.pos.get('selectedOrder').addProduct(product);
                    if (product.get('property_ids').length > 0)
                        self.show_selector(product);
                }
            },
            this._super(parent, options);
        },
        show_selector: function(product){
            property_selector = new module.PropertySelector(this,{product:product,draggable:false})
            property_selector.appendTo($('.point-of-sale'));             
        },
    });

    module.PropertySelector = module.BasePopup.extend({
        template: 'PropertySelector',
        init: function(parent, options){
            this._super(parent, options);
            this.step = 0;
            this.productPropertyWidgets = []
            this.orderLine = this.pos.get('selectedOrder').getSelectedLine();
            this.product_properties = this.load_properties();
            this.current = this.product_properties.at(0);
        },
        load_properties: function(){
            var self = this;
            var product = this.orderLine.get_product();
            product_properties = this.pos.get('product_properties');
            properties = new module.ProductPropertyList();
            _.each(product.get('property_ids'), function(id){
                properties.push(product_properties.get(id));
            })
            return product_properties;
        },
        renderElement: function(){
            this._super();
            var self = this;
            
            for(var i = 0, len = this.productPropertyWidgets.length; i < len; i++){
                this.productPropertyWidgets[i].destroy();
            }
            this.productPropertyWidgets = []; 
            _.each(this.current.get('products').models, function(p){
                var widget = new  module.ProductPropertyWidget(this, {model: p});
                self.productPropertyWidgets.push(widget); 
                widget.appendTo(self.$('.product-list'));                     
            });           
        },
        closePopup:function(e){
            //Pendiente: Si es edicion no se debe borrar esta linea
            this.pos.get('selectedOrder').removeOrderline(this.orderLine);
            this._super();
        },
    });
    
    module.ProductPropertyWidget =  module.PosBaseWidget.extend({
        template: 'ProductPropertyWidget',
        init: function(parent, options) {
            this._super(parent,options);
            this.model = options.model;
            this.model.attributes.weight = options.weight;
        },
        renderElement: function(){
            this._super();
        },
    });
    
}
