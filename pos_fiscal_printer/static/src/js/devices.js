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

function pos_fiscal_printer_devices(instance,module){
    module.ProxyDevice.include({
        init: function(options){
            this._super()
            this.printer = {}
        },   
        set_printer:function(printer){
            this.printer = printer;
        }, 
        get_printer:function(){
            return this.printer;
        },
        message : function(name,params){
            var ret = new $.Deferred();
            var callbacks = this.notifications[name] || [];
            for(var i = 0; i < callbacks.length; i++){
                callbacks[i](params);
            }
            this.connection.rpc('/hw_proxy/' + name, params || {}).done(function(result) {
                ret.resolve(result);
            }).fail(function(error) {
                ret.reject(error);
            });
            return ret;
        },
        print_report_x: function(){
            return this.message('print_report_x_json', {printer: this.printer});
        },
        print_receipt: function(receipt){
            return this.message('print_receipt',{receipt: receipt, printer: this.printer});
        },
        check_printer_status : function(){
            return this.message('check_printer_status', {printer: this.printer})
        }
    })
}
