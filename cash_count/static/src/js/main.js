openerp.cash_count = function(instance) {
    var module = instance.point_of_sale;
    cash_count_models(instance, module);
    cash_count_screens(instance, module);
    cash_count_widgets(instance, module);
}