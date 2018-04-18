# -*- coding: utf-8 -*-
##############################################################################
#
#    Odex - Communications Management System.
#    Copyright (C) 2017 Expert Co. Ltd. (<http://exp-sa.com>).
#
##############################################################################
{
    'name' : 'Communications Management',
    'version' : '0.1',
    'sequence' : 4,
    'author' : 'Expert Co. Ltd.',
    'category' : 'Extending odoo base module',
    'description' : """
Odex - Communications Management System
========================================
Managing Communications Transcations flows
    """,
    'website': 'http://www.exp-sa.com',
    'depends' : ['base', 'base_odex', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',

        # data
        'data/cm_data.xml',

        'views/outgoing_transaction_view.xml',
        'views/incoming_transaction_view.xml',
        'views/internal_transaction_view.xml',
        'views/settings_view.xml',
        'views/actions_and_menus.xml',

        'wizards/forward_wizard.xml',
    ],
    'qweb' : [
    ],
    'external_dependencies': {'python': ['xlsxwriter']},
    'installable': True,
    'auto_install': False,
    'application': True,
}
