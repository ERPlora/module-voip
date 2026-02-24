from django.contrib import admin

from .models import CallLog

@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ['caller_number', 'callee_number', 'direction', 'status', 'started_at', 'created_at']
    search_fields = ['caller_number', 'callee_number', 'direction', 'status']
    readonly_fields = ['created_at', 'updated_at']

