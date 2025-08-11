from django.urls import path
from . import views

app_name = 'motd'

urlpatterns = [
    # New enhanced MOTD system URLs
    path('', views.motd_list, name='list'),
    path('widget/', views.dashboard_widget, name='dashboard_widget'),
    path('create/', views.motd_create, name='create'),

    # Original group/state MOTD system URL (separate path)
    path('dashboard/', views.motd_dashboard, name='motd-dashboard'),
]
