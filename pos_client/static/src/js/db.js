function openerp_pos_db_ex(instance, module){
    module.PosLS.include({
        init: function(options){
            this._super(options);           
        },
        add_customers: function(customers){
            var stored_customers = this.load('customers',{}); 
            if(!customers instanceof Array){
                customers = [customers];
            }
            for(var i = 0, len = customers.length; i < len; i++){
                var c = customers[i];
                c.vat = _.rest(c.vat,2).join('')
                stored_customers[c.vat] = c;
            }
            this.save('customers',stored_customers);
        },  
        add_customer:function(customer){
            var customers =  this.load('new-customers',{}); 
            customers[customer.vat] = customer
            this.save('new-customers',customers)
        },
        update_customer:function(customer){
            var customers =  this.load('new-customers',{}); 
            customers[customer.vat] = customer
            this.save('new-customers',customers)
        },
        search_customer: function(vat){
            c = this.load('updated-customers',{})[vat] || null;
            if (c==null)
                c = this.load('new-customers',{})[vat] || null;
            if (c == null)
                c = this.load('customers',{})[vat] || null;
            return c;
        },
        get_all_customers: function(){
            list = [];
            stored_customers = this.load('customers',{});
            for (var i in stored_customers) {
                list.push(stored_customers[i]);
            }
            return list;
        },
        get_all_new_customers: function(){
            list = [];
            stored_customers = this.load('new-customers',{});
            for (var i in stored_customers) {
                list.push(stored_customers[i]);
            }
            return list;
        },
    })
}
