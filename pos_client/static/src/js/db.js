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
            var new_customers =  this.load('new-customers',{}); 
            new_customers[customer.vat] = customer
            this.save('new-customers',new_customers)
        },        
        update_customer:function(customer){
            var updated_customers =  this.load('updated-customers',{}); 
            updated_customers[customer.vat] = customer;
            this.save('updated-customers',updated_customers);
        },
        remove_created_customer:function(vat){
            var customers =  this.load('customers',{}); 
            var new_customers =  this.load('new-customers',{}); 
            customers[vat] = new_customers[vat]
            new_customers = _.filter(new_customers, function(customer){
                return customer.vat !== vat;
            });
            this.save('customers',customers);
            this.save('new-customers',new_customers);        
        },
        remove_updated_customer:function(vat){
            var customers =  this.load('customers',{}); 
            var updated_customers =  this.load('updated-customers',{});              
            customers[vat] = _.extend(customers[vat],updated_customers[vat]);
            
            updated_customers = _.filter(updated_customers, function(customer){
                return customer.vat !== vat;
            });
           
            this.save('customers',customers);
            this.save('updated-customers',updated_customers);        
        },
        search_customer: function(vat){
            updated_customers = this.load('updated-customers',{});
            new_customers = this.load('new-customers',{});
            customers = this.load('customers',{})
            return (updated_customers[vat] || new_customers[vat] || 
                    customers[vat] || null);
        },
        get_customers: function(){
            list = [];
            customers = this.load('customers',{});
            for (var i in customers) {
                list.push(customers[i]);
            }
            return list;
        },
        get_new_customers: function(){
            list = [];
            new_customers = this.load('new-customers',{});
            for (var i in new_customers) {
                list.push(new_customers[i]);
            }
            return list;
        },
        get_updated_customers: function(){
            list = [];
            updated_customers = this.load('updated-customers',{});
            for (var i in updated_customers) {
                list.push(updated_customers[i]);
            }
            return list;
        },
    })
}
