{
    # Theme information
    'name' : 'Material Backend Theme v8',
    'category' : 'Theme/Backend',
    'version' : '1.1.19',
    'summary': 'Backend, Clean, Modern, Material, Theme',
    'description': """
Material Backend Theme v8
=================
The visual and usability renovation odoo backend.
Designed in best possible look with flat, clean and clear design.
    """,
    'images': ['static/description/theme.jpg'],

    # Dependencies
    'depends': [
        'web',
        'base_odex',
    ],
    'external_dependencies': {},

    # Views
    'data': [
	   'views/backend.xml'
    ],

    # Author
    'author' : 'Expert',
    'website' : 'http://exp-sa.com',

    # Technical
    'installable': True,
    'auto_install': False,
    'application': False,

    # Market
    'license': 'Other proprietary',
    'live_test_url': 'http://8cells.com:8088/web/login',
    'currency': 'EUR',
    'price': 9000.00
}
