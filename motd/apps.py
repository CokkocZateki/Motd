# Django
from django.apps import AppConfig


class MotdConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "motd"
    label = "motd"
    verbose_name = "Message of the Day"

    def ready(self):
        pass

    default_auto_field = "django.db.models.BigAutoField"
    name = "motd"
    verbose_name = "MOTD Dashboard"
