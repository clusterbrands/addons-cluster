
# -*- encoding: utf-8 -*-
#
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
# Credits######################################################
#    Coded by: Coorporacion ClusterBrands C.A
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
{
    'name': "Payment Instrument",
    'category': "Generic Modules/Accounting",
    'version': "1.0",
    'depends': ['point_of_sale','pos_base'],
    'author': "Coorporacion ClusterBrands C.A",
    'description': """

This module allows the cash count for each payment method
in the POS

Main features
-------------

* The POS only can be closed by a manager if the final balance differs from the theoretical
* The difference is automatically adjusted to the appropriate account
* Show the number of transactions for each payment method

Note:
-----

You need to configure "Profit Account" and "Los Account"
for the journals
""",
    'data': [
        'view/account_view.xml',
        'view/payment_instrument_view.xml',
        'view/point_of_sale_view.xml',
        'view/account_view.xml',
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
    'qweb': ['static/src/xml/payment_instrument.xml'],
}
