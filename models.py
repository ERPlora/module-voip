from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

CALL_STATUS = [
    ('completed', _('Completed')),
    ('missed', _('Missed')),
    ('voicemail', _('Voicemail')),
    ('busy', _('Busy')),
    ('failed', _('Failed')),
]

class CallLog(HubBaseModel):
    caller_number = models.CharField(max_length=50, verbose_name=_('Caller Number'))
    callee_number = models.CharField(max_length=50, verbose_name=_('Callee Number'))
    direction = models.CharField(max_length=10, default='inbound', verbose_name=_('Direction'))
    status = models.CharField(max_length=20, default='completed', choices=CALL_STATUS, verbose_name=_('Status'))
    started_at = models.DateTimeField(verbose_name=_('Started At'))
    duration_seconds = models.PositiveIntegerField(default=0, verbose_name=_('Duration Seconds'))
    agent_id = models.UUIDField(null=True, blank=True, verbose_name=_('Agent Id'))
    recording_url = models.URLField(blank=True, verbose_name=_('Recording Url'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'voip_calllog'

    def __str__(self):
        return str(self.id)

