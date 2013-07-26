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

function pos_fiscal_printer_screens(instance,module){
    
    module.PaymentScreenWidget.include({
               
        validateCurrentOrder : function(){
            var self = this
            var currentOrder = this.pos.get('selectedOrder');           
            if(this.pos.iface_print_via_proxy){
                this.pos.proxy.print_receipt(currentOrder.export_for_printing())
                .done(function(response){
                    if (response.status == "ok"){
                        currentOrder.set_invoice_printer(response.serial)
                        currentOrder.set_fiscal_printer(response.receipt_id)
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
}
