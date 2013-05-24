/*
***************************************************************************
*    Module Writen to OpenERP, Open Source Management Solution
*    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
*    All Rights Reserved
***************Credits******************************************************
*    Coded by: Eduardo Ochoa    <eduardo.ochoa@clusterbrands.com.ve>
*                               <elos3000@gmail.com>
*****************************************************************************
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Affero General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Affero General Public License for more details.
*
*    You should have received a copy of the GNU Affero General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

function openerp_pos_db_ex(instance, module){ 

    module.PosLS.include({
        init: function(options){
            this._super(options);
            this.customer_list_search_strings = '';
            
        },
        add_customers: function(customers){
            var stored_customers = this.load('customers',{}); 

            if(!customers instanceof Array){
                customers = [customers];
            }
            for(var i = 0, len = customers.length; i < len; i++){
                var c = customers[i];
                this.customer_list_search_strings += this._customer_search_string(c);
                stored_customers[c.id] = c;
            }
            this.save('customers',stored_customers);
        },
        _customer_search_string: function(customer){
            var str = '' + customer.id + ':' + customer.name;
            if(customer.vat){
                str += '|' + customer.vat;
            }
            if(customer.email){
                str += '|' + customer.email;
            }
            if(customer.phone){
                str += '|' + customer.phone;
            }
            if(customer.mobile){
                str += '|' + customer.mobile;
            }
            return str + '\n';
        },
        add_customers: function(customers){
            var stored_customers = this.load('customers',{}); 

            if(!customers instanceof Array){
                customers = [customers];
            }
            for(var i = 0, len = customers.length; i < len; i++){
                var c = customers[i];
                this.customer_list_search_strings += this._customer_search_string(c);
                stored_customers[c.id] = c;
            }
            this.save('customers',stored_customers);
        },
        get_customer_by_id: function(id){
            return this.load('customers',{})[id];
        },
        get_all_customers: function(){
            list = [];
            stored_customers = this.load('customers',{});
            for (var i in stored_customers) {
                list.push(stored_customers[i]);
            }
            return list;
        },
        search_customers: function(query){
            var re = RegExp("([0-9]+):.*?"+query,"gi");
            var results = [];
            for(var i = 0; i < this.limit; i++){
                r = re.exec(this.customer_list_search_strings);
                if(r){
                    var id = Number(r[1]);
                    results.push(this.get_customer_by_id(id));
                }else{
                    break;
                }
            }
            return results;
        },
    
    })

 
}
