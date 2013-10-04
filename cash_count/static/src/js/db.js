function cash_count_db(instance, module){
    module.PosLS.include({
        set_current_cashier: function(cashier){
            this.save('current-cashier',cashier);
        },
    });
}