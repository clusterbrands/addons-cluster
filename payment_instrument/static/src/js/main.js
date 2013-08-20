openerp.payment_instrument = function(instance) {
    var module = instance.point_of_sale;
    payment_instrument_models(instance, module);
    payment_instrument_widgets(instance,module);
    payment_instrument_screens(instance, module);
}