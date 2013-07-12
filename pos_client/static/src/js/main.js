openerp.pos_client = function(instance){
    var module = instance.point_of_sale;
    pos_client_db(instance, module)
    pos_client_models(instance,module);
    pos_client_screens(instance,module);
    pos_client_widgets(instance,module); 
    instance.pos_client = module;
}
