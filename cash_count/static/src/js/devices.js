function cash_count_devices(instance,module){ 
    module.ProxyDevice.include({
        print_x_report: function(){
            return this.message('print_x_report');
        },
    });
}