function openerp_pos_devices_ex(instance,module){
    module.ProxyDevice.include({
        check_printer_status : function(printer){
            return this.message('check_printer_status',{printer:printer})
        }
    })
}
