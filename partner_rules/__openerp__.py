#!/usr/bin/python
# -*- encoding: utf-8 -*-
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#    Author: Cluster Brands
#    Copyright 2013 Cluster Brands
#    Designed By: Jose J Perez M <jose.perez@clusterbrands.com>
#    Coded by: Eduardo Ochoa  <eduardo.ochoa@clusterbrands.com.ve>
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  
{                                                                                  
    'name' : 'Partner Rule',
    'category': 'Generic Modules',                                                                   
    'version' : '1.0',                                                             
    'author' : 'Vauxoo/Cluster Brands',
    'website': 'http://www.clusterbrands.com',                                                                                                              
    'description' : """                                                            

                                                                                   
    """,                                                                           
    'depends' : [
        'base',
        'account',
        'purchase',
        'sale',
    ],                                                                
    'data': [                                                                      
        'data/access_rule_data.xml',
        'view/partner_view.xml',
    ],                                                                                 
    'js': [                                                                        
    ],                                                                                 
    'qweb' : [                                                                     
    ],                                                                                 
    'css':[                                                                        
    ],                                                                                 
    'demo': [                                                                      
    ],                                                                                 
    'test': [                                                                      
    ],                                                                                                                                                                                                  
    'installable': True,                                                           
    'auto_install': False,                                                         
}                                                                                  
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: 
