from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CallLog

class CallLogForm(forms.ModelForm):
    class Meta:
        model = CallLog
        fields = ['caller_number', 'callee_number', 'direction', 'status', 'started_at', 'duration_seconds', 'agent_id', 'recording_url', 'notes']
        widgets = {
            'caller_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'callee_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'direction': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'started_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'duration_seconds': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'agent_id': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'recording_url': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'url'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

