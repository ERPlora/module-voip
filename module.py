from django.utils.translation import gettext_lazy as _

MODULE_ID = 'voip'
MODULE_NAME = _('VoIP & Telephony')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'call-outline'
MODULE_DESCRIPTION = _('VoIP integration, call logging and telephony')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'communication'

MENU = {
    'label': _('VoIP & Telephony'),
    'icon': 'call-outline',
    'order': 66,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Call Log'), 'icon': 'call-outline', 'id': 'calls'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'voip.view_calllog',
'voip.add_calllog',
'voip.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "add_calllog",
        "view_calllog",
    ],
    "employee": [
        "add_calllog",
        "view_calllog",
    ],
}
