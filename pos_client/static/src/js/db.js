function openerp_pos_db_ex(instance, module){
    module.PosLS.include({
        add_customers: function(customers){
            var stored_customers = this.load('customers',{}); 

            if(!customers instanceof Array){
                customers = [customers];
            }
            for(var i = 0, len = customers.length; i < len; i++){
                var c = customers[i];
                //this.customer_list_search_strings += this._customer_search_string(c);
                stored_customers[c.id] = c;
            }
            this.save('customers',stored_customers);
        },
    })
}
