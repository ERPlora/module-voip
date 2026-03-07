"""
VoIP & Telephony Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import CallLog

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('voip', 'dashboard')
@htmx_view('voip/pages/index.html', 'voip/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_call_logs': CallLog.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# CallLog
# ======================================================================

CALL_LOG_SORT_FIELDS = {
    'status': 'status',
    'duration_seconds': 'duration_seconds',
    'caller_number': 'caller_number',
    'callee_number': 'callee_number',
    'direction': 'direction',
    'started_at': 'started_at',
    'created_at': 'created_at',
}

def _build_call_logs_context(hub_id, per_page=10):
    qs = CallLog.objects.filter(hub_id=hub_id, is_deleted=False).order_by('status')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'call_logs': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'status',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_call_logs_list(request, hub_id, per_page=10):
    ctx = _build_call_logs_context(hub_id, per_page)
    return django_render(request, 'voip/partials/call_logs_list.html', ctx)

@login_required
@with_module_nav('voip', 'calls')
@htmx_view('voip/pages/call_logs.html', 'voip/partials/call_logs_content.html')
def call_logs_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'status')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = CallLog.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(caller_number__icontains=search_query) | Q(callee_number__icontains=search_query) | Q(direction__icontains=search_query) | Q(status__icontains=search_query))

    order_by = CALL_LOG_SORT_FIELDS.get(sort_field, 'status')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['status', 'duration_seconds', 'caller_number', 'callee_number', 'direction', 'started_at']
        headers = ['Status', 'Duration Seconds', 'Caller Number', 'Callee Number', 'Direction', 'Started At']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='call_logs.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='call_logs.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'voip/partials/call_logs_list.html', {
            'call_logs': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'call_logs': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
@htmx_view('voip/pages/call_log_add.html', 'voip/partials/call_log_add_content.html')
def call_log_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        caller_number = request.POST.get('caller_number', '').strip()
        callee_number = request.POST.get('callee_number', '').strip()
        direction = request.POST.get('direction', '').strip()
        status = request.POST.get('status', '').strip()
        started_at = request.POST.get('started_at') or None
        duration_seconds = int(request.POST.get('duration_seconds', 0) or 0)
        agent_id = request.POST.get('agent_id', '').strip()
        recording_url = request.POST.get('recording_url', '').strip()
        notes = request.POST.get('notes', '').strip()
        obj = CallLog(hub_id=hub_id)
        obj.caller_number = caller_number
        obj.callee_number = callee_number
        obj.direction = direction
        obj.status = status
        obj.started_at = started_at
        obj.duration_seconds = duration_seconds
        obj.agent_id = agent_id
        obj.recording_url = recording_url
        obj.notes = notes
        obj.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('voip:call_logs_list')
        return response
    return {}

@login_required
@htmx_view('voip/pages/call_log_edit.html', 'voip/partials/call_log_edit_content.html')
def call_log_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(CallLog, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.caller_number = request.POST.get('caller_number', '').strip()
        obj.callee_number = request.POST.get('callee_number', '').strip()
        obj.direction = request.POST.get('direction', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.started_at = request.POST.get('started_at') or None
        obj.duration_seconds = int(request.POST.get('duration_seconds', 0) or 0)
        obj.agent_id = request.POST.get('agent_id', '').strip()
        obj.recording_url = request.POST.get('recording_url', '').strip()
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_call_logs_list(request, hub_id)
    return {'obj': obj}

@login_required
@require_POST
def call_log_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(CallLog, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_call_logs_list(request, hub_id)

@login_required
@require_POST
def call_logs_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = CallLog.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_call_logs_list(request, hub_id)


@login_required
@permission_required('voip.manage_settings')
@with_module_nav('voip', 'settings')
@htmx_view('voip/pages/settings.html', 'voip/partials/settings_content.html')
def settings_view(request):
    return {}

