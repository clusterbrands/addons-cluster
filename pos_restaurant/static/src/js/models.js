function pos_restaurant_models(instance, module){
    
    module.PosModel = module.PosModel.extend({
        load_server_data : function(){
            var self= this;
            loaded = this._super().then(function(){
                return self.fetch('pos_restaurant.product_property',[],[]);
            }).then(function(properties){
                self.add_product_properties(properties);
            });;
            return loaded
        },
        fetch: function(model, fields, domain, ctx){
            if (model == 'product.product')
                fields.push('property_ids')
            return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all()
        },
        add_product_properties: function(properties){
            var self= this;
            var product_properties = new module.ProductPropertyList();
            _.each(properties, function(property){
                var products = new Backbone.Collection();
                _.each(property.product_ids, function(id){
                    products.add(self.db.get_product_by_id(id));
                });
                product_properties.push({
                    'id': property.id,
                    'name': property.name,
                    'single_choice': property.single_choice,
                    'sequence': property.sequence,
                    'products': products,
                })
            });
            this.set('product_properties', product_properties);
        }
    });

    module.ProductProperty = Backbone.Model.extend({
        defaults: {
            'name': '',
            'single_choice': false,
            'sequence': 0,
            'products': new Backbone.Collection(),
        },
        initialize :function(attrs){
            this._super(attrs);
        },
    });

    module.ProductPropertyList = Backbone.Collection.extend({
        model: module.ProductProperty,
        sort_key: 'id',
        comparator: function(item) {
            return item.get(this.sort_key);
        },
        sortByField: function(fieldName) {
            this.sort_key = fieldName;
            this.sort();
        },
    });

    // module.Propertyline = module.Orderline.extend({
    // });

    module.Orderline = module.Orderline.extend({
        initialize :function(attrs, options){
            this._super(attrs, options);
        },
    });
}