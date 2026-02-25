from django.urls import path
from . import views

app_name = 'voip'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('calls/', views.call_logs_list, name='calls'),


    # CallLog
    path('call_logs/', views.call_logs_list, name='call_logs_list'),
    path('call_logs/add/', views.call_log_add, name='call_log_add'),
    path('call_logs/<uuid:pk>/edit/', views.call_log_edit, name='call_log_edit'),
    path('call_logs/<uuid:pk>/delete/', views.call_log_delete, name='call_log_delete'),
    path('call_logs/bulk/', views.call_logs_bulk_action, name='call_logs_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
