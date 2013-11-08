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
    'name': "Payment Instrument",
    'category': "Point of Sale",
    'version': "1.0",
    'author': 'Cluster Brands',
    'website': 'http://www.clusterbrands.com',
    'description': """

This module allows you to add multiple POS payment instruments. 
For example, credit cards, debits cards, feed tickets.

Main features
-------------

* You can define five instrument types (card, ticket, coupon and giftcard)
* Each payment instrument is associated with a journal.
* A payment instrument is defined by one or more rules.
* A rule has a criterion of application and type of calculation

Note:
-----
 -Each payment instrument must be defined in a bank type journal
 -A payment instrument must contain at least one rule

""",
    'depends': [
        'point_of_sale',
        'pos_base'
    ],
    'data': [
        'view/account_view.xml',
        'view/payment_instrument_view.xml',
        'view/point_of_sale_view.xml',
    ],
    'js': [
        'static/src/js/backbone-super-min.js',
        'static/src/js/models.js',
        'static/src/js/screens.js',
        'static/src/js/widgets.js',
        'static/src/js/main.js',
    ],
    'css': [
        'static/src/css/pos.css',
    ],
    'qweb': [
        'static/src/xml/payment_instrument.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
