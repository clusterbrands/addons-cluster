openerp.pos_restaurant = function(instance){
    var module = instance.point_of_sale;
    pos_restaurant_models(instance, module);
    pos_restaurant_widgets(instance, module);
    instance.pos_restaurant = module;
}