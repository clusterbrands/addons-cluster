openerp.pos_fiscal_printer = function(instance){
    var module = instance.point_of_sale
    var _super_ = module.PosModel.prototype.initialize
    module.PosModel.prototype.initialize = function(session, attributes) {
            console.debug("this method is overwritten")
            _super_.call(this,session, attributes)
    }
}
