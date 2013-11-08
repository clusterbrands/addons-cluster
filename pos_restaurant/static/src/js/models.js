function pos_restaurant_models(instance, module){

    module.PosModel = module.PosModel.extend({
        load_server_data : function(){
            self = this
            loaded = this._super().then(function(){
                return self.fetch('pos_restaurant.product_property',[],[]);
            }).then(function(product_properties){
                product_properties = new module.ProductPropertiesCollection(product_properties)
                self.set('product_properties',product_properties);
            });
            return loaded 
        },
        fetch: function(model, fields, domain, ctx){
            if (model == 'product.product')
                fields.push('property_ids')
            return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all()
        },
    }); 

    module.ProductPropertiesCollection = Backbone.Collection.extend({
        sort_key: 'id',
        comparator: function(item) {
            return item.get(this.sort_key);
        },
        sortByField: function(fieldName) {
            this.sort_key = fieldName;
            this.sort();
        }
    });


}