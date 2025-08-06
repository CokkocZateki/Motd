from django.urls import path
from . import views

app_name = 'motd'

urlpatterns = [
    path('', views.motd_list, name='list'),
    path('widget/', views.dashboard_widget, name='dashboard_widget'),
]
