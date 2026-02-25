# VoIP & Telephony Module

VoIP integration, call logging, and telephony management for tracking inbound and outbound calls.

## Features

- Call log with inbound/outbound direction tracking
- Call status tracking (completed, missed, voicemail, busy, failed)
- Call duration recording in seconds
- Agent assignment via UUID reference
- Optional call recording URL storage
- Notes per call entry
- Dashboard with call activity overview

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > VoIP & Telephony > Settings**

## Usage

Access via: **Menu > VoIP & Telephony**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/voip/dashboard/` | Overview of call activity and statistics |
| Call Log | `/m/voip/calls/` | List and manage call log entries |
| Settings | `/m/voip/settings/` | Configure VoIP and telephony settings |

## Models

| Model | Description |
|-------|-------------|
| `CallLog` | Records individual calls with caller/callee numbers, direction, status, duration, agent assignment, recording URL, and notes |

## Permissions

| Permission | Description |
|------------|-------------|
| `voip.view_calllog` | View call log entries |
| `voip.add_calllog` | Create new call log entries |
| `voip.manage_settings` | Manage VoIP module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
