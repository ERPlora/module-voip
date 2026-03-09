# VoIP & Telephony

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `voip` |
| **Version** | `1.0.0` |
| **Icon** | `call-outline` |
| **Dependencies** | None |

## Models

### `CallLog`

CallLog(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, caller_number, callee_number, direction, status, started_at, duration_seconds, agent_id, recording_url, notes)

| Field | Type | Details |
|-------|------|---------|
| `caller_number` | CharField | max_length=50 |
| `callee_number` | CharField | max_length=50 |
| `direction` | CharField | max_length=10 |
| `status` | CharField | max_length=20, choices: completed, missed, voicemail, busy, failed |
| `started_at` | DateTimeField |  |
| `duration_seconds` | PositiveIntegerField |  |
| `agent_id` | UUIDField | max_length=32, optional |
| `recording_url` | URLField | max_length=200, optional |
| `notes` | TextField | optional |

## URL Endpoints

Base path: `/m/voip/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `calls/` | `calls` | GET |
| `call_logs/` | `call_logs_list` | GET |
| `call_logs/add/` | `call_log_add` | GET/POST |
| `call_logs/<uuid:pk>/edit/` | `call_log_edit` | GET |
| `call_logs/<uuid:pk>/delete/` | `call_log_delete` | GET/POST |
| `call_logs/bulk/` | `call_logs_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `voip.view_calllog` | View Calllog |
| `voip.add_calllog` | Add Calllog |
| `voip.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_calllog`, `view_calllog`
- **employee**: `add_calllog`, `view_calllog`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Call Log | `call-outline` | `calls` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_call_logs`

List VoIP call logs.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `direction` | string | No | inbound, outbound |
| `status` | string | No | completed, missed, voicemail, busy, failed |
| `limit` | integer | No |  |

### `get_call_log`

Get detailed call log info including recording URL and notes.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `call_id` | string | Yes | Call log ID |

### `add_call_notes`

Add or update notes on a call log.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `call_id` | string | Yes | Call log ID |
| `notes` | string | Yes | Notes to add |

### `get_call_stats`

Get call statistics: total calls, missed rate, average duration.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `period` | string | No | today, this_week, this_month (default: today) |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  voip/
    css/
    js/
templates/
  voip/
    pages/
      call_log_add.html
      call_log_edit.html
      call_logs.html
      calls.html
      dashboard.html
      index.html
      settings.html
    partials/
      call_log_add_content.html
      call_log_edit_content.html
      call_logs_content.html
      call_logs_list.html
      calls_content.html
      dashboard_content.html
      panel_call_log_add.html
      panel_call_log_edit.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
