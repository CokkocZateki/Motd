from django.urls import path
from . import views

urlpatterns = [
    path("", views.motd_dashboard, name="motd-dashboard"),
]
