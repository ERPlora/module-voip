"""
VoIP & Telephony Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('voip', 'dashboard')
@htmx_view('voip/pages/dashboard.html', 'voip/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('voip', 'calls')
@htmx_view('voip/pages/calls.html', 'voip/partials/calls_content.html')
def calls(request):
    """Call Log view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('voip', 'settings')
@htmx_view('voip/pages/settings.html', 'voip/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

