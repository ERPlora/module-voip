from django.urls import path
from . import views

app_name = 'voip'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('calls/', views.calls, name='calls'),
    path('settings/', views.settings, name='settings'),
]
