# Django
from django.urls import path

# AA Motd
from motd import views

app_name: str = "motd"

urlpatterns = [
    path("", views.motd_list, name="list"),
    path("widget/", views.dashboard_widget, name="dashboard_widget"),
    path("create/", views.motd_create, name="create"),
    path("edit/<int:pk>/", views.motd_edit, name="edit"),
    path("delete/<int:pk>/", views.motd_delete, name="delete"),
]
