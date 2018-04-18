# -*- coding: utf-8 -*-
##############################################################################
#
#    AFAQ, (Odex - Extending the base module).
#    Copyright (C) 2017 Expert Co. Ltd. (<http://exp-sa.com>).
#
##############################################################################
{
    'name' : 'Odex - Base Module',
    'version' : '0.1',
    'author' : 'Expert Co. Ltd.',
    'category' : 'Extending odoo base module',
    'description' : """
Odex - Extending the base module
=================================
Extending the Odoo's base module by adding a cross-apps models e.g. `res.country.city`.
any new module should depend in this module so that developer can reuse it.
    """,
    'website': 'http://www.exp-sa.com',
    'depends' : ['base'],
    'data': [
        'views/assets_backend.xml',
        'security/ir.model.access.csv',
        'views/res_city_view.xml',
        'views/menus_and_actions.xml',
    ],
    'qweb' : [
        'static/src/xml/base_odex.xml',
    ],
    'external_dependencies': {'python': ['xlsxwriter']},
    'installable': True,
    'auto_install': False,
}
