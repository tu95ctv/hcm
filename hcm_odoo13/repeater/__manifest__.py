# -*- coding: utf-8 -*-
{
    'name': "repeater",
    'summary': "Quản lý Repeater cho NET2",
    'description': "Quản lý Repeater cho NET2",
    'author': "NDT",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/image.xml',
        'views/repeater.xml',
        'views/repeater_views_full.xml',
        'views/department.xml',
        'views/user.xml',
        'views/res_config_settings_views.xml',

    ],
    'demo': [
    ],
}