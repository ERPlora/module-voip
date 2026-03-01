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
