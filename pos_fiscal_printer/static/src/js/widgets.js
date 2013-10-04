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

function pos_fiscal_printer_widgets(instance, module){ 
    
    module.PosWidget.include({
        build_widgets: function(){
            this._super()
            var self = this;
                        
            this.not_printer_error_popup = new module.NotPrinterErrorPopupWidget(this,{})
            this.not_printer_error_popup.appendTo($('.point-of-sale'));
            
            this.printer_error_popup = new module.PrinterErrorPopupWidget(this,{})
            this.printer_error_popup.appendTo($('.point-of-sale'));
            
            this.print_error_popup = new module.PrintErrorPopupWidget(this,{})
            this.print_error_popup.appendTo($('.point-of-sale'));
            
            this.screen_selector.add_popup('not-printer-error',this.not_printer_error_popup)
            this.screen_selector.add_popup('printer-error',this.printer_error_popup)
            this.screen_selector.add_popup('print-error',this.print_error_popup)
        }
    })
      
    module.PrinterErrorPopupWidget = module.PopUpWidget.extend({
        template:'PrinterErrorPopupWidget',
        show: function(){
            self = this
            this._super();
            this.$('.retry').off('click').click(_.bind(this.click_retry,this))
            this.$('.close').off('click').click(_.bind(this.click_close,this))            
        },
        click_retry :function(){
            self.pos_widget.screen_selector.close_popup();
            self.pos_widget.check_printer_status()
        },
        click_close :function(){
            this.pos_widget.try_close()
        },        
        set_message : function(message){
            this.message = message
            this.renderElement();
        }        
        
    }); 
    
    module.PrintErrorPopupWidget = module.PopUpWidget.extend({
        template:'PrintErrorPopupWidget',
        show: function(){
            self = this
            this._super();
            this.$('.close').off('click').click(_.bind(this.click_close,this))            
        },
        click_close :function(){
            self.pos_widget.screen_selector.close_popup();
        },        
        set_message : function(message){
            this.message = message
            this.renderElement();
        }     
    })
           
    
    module.NotPrinterErrorPopupWidget = module.PopUpWidget.extend({
        template:'NotPrinterErrorPopupWidget',
        show: function(){
            self = this
            this._super();
            this.$('.button').off('click').click(_.bind(this.click_close,this))
        },
        click_close :function(){
            this.pos_widget.try_close()
        },
      
    });
    
}
