#!/usr/bin/python
# -*- encoding: utf-8 -*-                                                       
############################################################################### 
#    Module Writen to OpenERP, Open Source Management Solution                  
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).                 
#    All Rights Reserved                                                        
# Credits######################################################                 
#    Coded by: Luis Escobar <luis@vauxoo.com>                                      
#    Audited by:  Humberto Arocha <humbertoarocha@gmail.com>                    
############################################################################### 
#    This program is free software: you can redistribute it and/or modify          
#    it under the terms of the GNU Affero General Public License as published   
#    by the Free Software Foundation, either version 3 of the License, or          
#    (at your option) any later version.                                        
#                                                                               
#    This program is distributed in the hope that it will be useful,            
#    but WITHOUT ANY WARRANTY; without even the implied warranty of             
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              
#    GNU Affero General Public License for more details.                        
#                                                                               
#    You should have received a copy of the GNU Affero General Public License   
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.         
###############################################################################

{                                                                                  
    "name": "Pos Debit and Credit Card Payment Instrument",
    "version": "0.1",
    "depends": ["base", "point_of_sale","payment_instrument"],
    "summary": "",
    "author": "Vauxoo",
    "description": """
    Add a process in POS to work with debit and credit card payments instrument.

    Note:
     To install this module is required to have linked the modules lp: addons-cluster.

-------------------------------------------------------------------------------

     Para Configurar este modulo se requiere hacer lo siguiente:
        - En cada 'Payment Instrument' del Journal se debe agregar por lo menos un 'Rule' 
          de tipo 'Percentage'.
        - Todos los Rules deben contener una cuenta contable el cual se imputara el monto
          de dicho calculo.
        - Los 'Rule' de tipo 'percentage' son para realizar internamente el calculo de 
          alguna comision o impuesto retenido, se requiere colocar el porcentaje que desee
          que se calcule con respecto al monto total del Bank Statement.
        - Se requiere colocar en el campo 'Bank Account' en el journal la cuenta bancaria
          donde se cargará el monto a depositar por el banco.

     Ejemplo de Configuracion:

        Teniendo el instrumento 'Credito' en el Journal 'Bank Journal' que previamente debe 
        estar configurado para que sea un tipo de pago del POS, se realiza lo siguiente:
           1.- Se Agrega un Rule llamado 'Comision Bancaria'
           2.- Se selecciona en el campo 'Condition Based on' el valor 'Always True'
           3.- Se selecciona en el campo 'Imputing Condition Account' la cuenta contable
             que contendrá el monto del porcentaje que el banco toma como comision por el
             servicio de Punto de Venta.
           4.- Se selecciona en el campo 'Amount Type' el valor 'Percentage (%)'.
           5.- Coloque en el campo 'Percentage (%)' el porcentaje que el banco toma como 
             comision por el servicio.
           6.- Se presiona el boton 'Save & Close'
           7.- Para Agregar otra comision o un ISLR que retenga el banco se debe repetir 
             los pasos del 1 al 6 cambiando en el paso 1 el nombre apropiado para esta 
             comision o impuesto y en el paso 3 colocar la cuenta contable que corresponda.

           Para el instrumento de "Debito" solo es necesario el Rule de comision bancaria
           ya que esta transaccion no genera ISLR

           Recuerde que debe configurar en el Journal, el campo de la cuenta contable de la 
           cuenta bancaria donde el banco realiza el deposito (Bank Account)

         Luego que realice las ventas y desee realizar el cierre de un lote del Punto de Venta 
         se debe abrir el 'Bank statement' que desee procesar y presione el boton 'Close Lot'

    """,                      
    "website": "http://vauxoo.com",                                             
    "category": "Point Of Sale",                                                
    "data": [                                                                   
        #'view/point_of_sale_view.xml',
        'wizard/close_lot_view.xml',
        'view/account_view.xml',
    ],                                                                          
    'js':[
    ],                                                                          
    'css': [
    ],                                                                          
    'qweb': [ 
    ],                                                                          
    "active": False,                                                            
    "installable": True,                                                        
}
