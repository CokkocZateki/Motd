# Django
from django.urls import path

from . import views

app_name: str = "motd"

urlpatterns = [
    path("", views.motd_list, name="list"),
    path("widget/", views.dashboard_widget, name="dashboard_widget"),
    path("create/", views.motd_create, name="create"),
    path("edit/<int:pk>/", views.motd_edit, name="edit"),
    path("delete/<int:pk>/", views.motd_delete, name="delete"),
    # Legacy group/state MOTD system
    path("dashboard/", views.motd_dashboard, name="motd-dashboard"),
]
