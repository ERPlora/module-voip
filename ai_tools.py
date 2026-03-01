"""AI tools for the VoIP module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListCallLogs(AssistantTool):
    name = "list_call_logs"
    description = "List VoIP call logs."
    module_id = "voip"
    required_permission = "voip.view_calllog"
    parameters = {
        "type": "object",
        "properties": {
            "direction": {"type": "string", "description": "inbound, outbound"},
            "status": {"type": "string", "description": "completed, missed, voicemail, busy, failed"},
            "limit": {"type": "integer"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from voip.models import CallLog
        qs = CallLog.objects.all()
        if args.get('direction'):
            qs = qs.filter(direction=args['direction'])
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        limit = args.get('limit', 20)
        return {"calls": [{"id": str(c.id), "caller_number": c.caller_number, "callee_number": c.callee_number, "direction": c.direction, "status": c.status, "started_at": c.started_at.isoformat() if c.started_at else None, "duration_seconds": c.duration_seconds} for c in qs.order_by('-started_at')[:limit]]}


@register_tool
class GetCallLog(AssistantTool):
    name = "get_call_log"
    description = "Get detailed call log info including recording URL and notes."
    module_id = "voip"
    required_permission = "voip.view_calllog"
    parameters = {
        "type": "object",
        "properties": {"call_id": {"type": "string", "description": "Call log ID"}},
        "required": ["call_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from voip.models import CallLog
        c = CallLog.objects.get(id=args['call_id'])
        return {
            "id": str(c.id), "caller_number": c.caller_number,
            "callee_number": c.callee_number, "direction": c.direction,
            "status": c.status, "started_at": c.started_at.isoformat() if c.started_at else None,
            "duration_seconds": c.duration_seconds, "agent_id": str(c.agent_id) if c.agent_id else None,
            "recording_url": c.recording_url if c.recording_url else None,
            "notes": c.notes,
        }


@register_tool
class AddCallNotes(AssistantTool):
    name = "add_call_notes"
    description = "Add or update notes on a call log."
    module_id = "voip"
    required_permission = "voip.change_calllog"
    parameters = {
        "type": "object",
        "properties": {
            "call_id": {"type": "string", "description": "Call log ID"},
            "notes": {"type": "string", "description": "Notes to add"},
        },
        "required": ["call_id", "notes"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from voip.models import CallLog
        c = CallLog.objects.get(id=args['call_id'])
        c.notes = args['notes']
        c.save(update_fields=['notes'])
        return {"id": str(c.id), "notes": c.notes, "updated": True}


@register_tool
class GetCallStats(AssistantTool):
    name = "get_call_stats"
    description = "Get call statistics: total calls, missed rate, average duration."
    module_id = "voip"
    required_permission = "voip.view_calllog"
    parameters = {
        "type": "object",
        "properties": {
            "period": {"type": "string", "description": "today, this_week, this_month (default: today)"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from datetime import date, timedelta
        from django.db.models import Avg, Count
        from voip.models import CallLog
        period = args.get('period', 'today')
        today = date.today()
        if period == 'this_week':
            start = today - timedelta(days=today.weekday())
        elif period == 'this_month':
            start = today.replace(day=1)
        else:
            start = today
        qs = CallLog.objects.filter(started_at__date__gte=start)
        total = qs.count()
        missed = qs.filter(status='missed').count()
        avg_duration = qs.filter(status='completed').aggregate(avg=Avg('duration_seconds'))['avg']
        by_direction = {
            'inbound': qs.filter(direction='inbound').count(),
            'outbound': qs.filter(direction='outbound').count(),
        }
        return {
            "period": period, "total_calls": total,
            "missed": missed, "missed_rate": f"{missed / total * 100:.1f}%" if total else "0%",
            "avg_duration_seconds": round(avg_duration) if avg_duration else 0,
            "by_direction": by_direction,
        }
