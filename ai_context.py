"""
AI context for the VoIP module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: VoIP

### Models

**CallLog**
- `caller_number` (CharField, max 50) — phone number of the caller
- `callee_number` (CharField, max 50) — phone number of the callee
- `direction` (CharField, default 'inbound') — 'inbound' or 'outbound'
- `status` (CharField) — choices: completed, missed, voicemail, busy, failed
- `started_at` (DateTimeField) — when the call started (must be set explicitly)
- `duration_seconds` (PositiveIntegerField, default 0) — call duration in seconds
- `agent_id` (UUIDField, nullable) — UUID of the staff member who handled the call
- `recording_url` (URLField, blank) — link to a call recording if available
- `notes` (TextField, blank) — internal notes about the call

### Key flows

1. **Log a call**: Create a CallLog record when a call is initiated or received. Set `direction`, both numbers, `started_at`, and `status`.
2. **After call**: Update `duration_seconds`, `status`, and optionally `recording_url` and `notes`.
3. **Query history**: Filter by `caller_number` or `callee_number` to find call history for a contact.
4. **Missed calls**: Filter `status='missed'` to show agents which calls need a callback.

### Relationships
- No FK to customers module — phone numbers are stored as plain text; match manually if needed
- `agent_id` is a UUID reference to a staff member (accounts.LocalUser), not a FK
- This module logs calls only; VoIP provider integration is handled externally
"""
