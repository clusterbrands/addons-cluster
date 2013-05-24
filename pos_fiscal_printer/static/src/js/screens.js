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

function openerp_pos_screens_ex(instance,module){
    
    module.PaymentScreenWidget.include({
               
        validateCurrentOrder : function(){
            var self = this
            var currentOrder = this.pos.get('selectedOrder');           
            if(this.pos.iface_print_via_proxy){
                this.pos.proxy.print_receipt(currentOrder.export_for_printing())
                .done(function(response){
                    if (response.status == "ok"){
                        console.debug(response)
                        currentOrder.set_printer_serial(response.serial)
                        currentOrder.set_printer_receipt_number(response.receipt_id)
                        self.pos.push_order(currentOrder.exportAsJSON()) 
                        self.pos.get('selectedOrder').destroy();
                    }else{
                        self.pos_widget.print_error_popup.set_message(response.error)
                        self.pos_widget.screen_selector.show_popup('print-error');
                    }
                })
            }else{
                this.pos_widget.screen_selector.set_current_screen(this.next_screen);
            } 
        }
    })

    module.SelectCustomerPopupWidget = module.PopUpWidget.extend({
        template:'SelectCustomerPopupWidget',        
        start: function(){
            this._super();
            var self = this;
            this.customer_list_widget = new module.CustomerListWidget(this,{
                click_customer_action: function(customer){
                    this.pos.get('selectedOrder').set_client(customer);
                    this.pos_widget.customername.refresh();
                    this.pos_widget.screen_selector.set_current_screen('products');
                },
            });
        },
        
        show: function(){
            this._super();
            var self = this;
            this.renderElement();
            
            this.customer_list_widget.replace($('.placeholder-CustomerListWidget'));

            this.$('.button.cancel').off('click').click(function(){
                self.pos_widget.screen_selector.set_current_screen('products');
            });
            
            this.customer_search();
        },

        // Customer search filter
        customer_search: function(){
            var self = this;

            // find all products belonging to the current category
            var customers = this.pos.db.get_all_customers();
            self.pos.get('customers').reset(customers);

            // filter customers according to the search string
            this.$('.customer-searchbox input').keyup(function(event){
                query = $(this).val().toLowerCase();
                if(query){
                    var customers = self.pos.db.search_customers(query);
                    self.pos.get('customers').reset(customers);
                    self.$('.customer-search-clear').fadeIn();
                    if(event.keyCode == 13){
                        var c = null;
                        if(customers.length == 1){
                            c = self.pos.get('customers').get(customers[0]);
                        }
                        if(c !== null){
                            self.pos_widget.select_customer_popup.customer_list_widget.click_customer_action(c);
                            self.$('.customer-search-clear').trigger('click');
                        }
                    }
                }else{
                    var customers = self.pos.db.get_all_customers();
                    self.pos.get('customers').reset(customers);
                    self.$('.customer-search-clear').fadeOut();
                }
            });

            this.$('.customer-searchbox input').click(function(){}); //Why ???

            //reset the search when clicking on reset
            this.$('.customer-search-clear').click(function(){
                var customers = self.pos.db.get_all_customers();
                self.pos.get('customers').reset(customers);
                self.$('.customer-searchbox input').val('').focus();
                self.$('.customer-search-clear').fadeOut();
            });
        },

    });
}
