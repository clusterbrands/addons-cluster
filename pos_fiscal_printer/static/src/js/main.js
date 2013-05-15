openerp.pos_fiscal_printer = function(instance){
    var module = instance.point_of_sale
    openerp_pos_db_ex(instance,module); 
    openerp_pos_models_ex(instance,module);
    openerp_pos_screens_ex(instance,module);
    openerp_pos_widgets_ex(instance,module); 
}
