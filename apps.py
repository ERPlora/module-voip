from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VoipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voip'
    label = 'voip'
    verbose_name = _('VoIP & Telephony')

    def ready(self):
        pass
