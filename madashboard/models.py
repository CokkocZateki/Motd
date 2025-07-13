from django.db import models
from django.contrib.auth.models import Group


class GroupMotd(models.Model):
    """Stores a message of the day for a specific group."""

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    message = models.TextField()
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Group MOTD"
        verbose_name_plural = "Group MOTDs"
        ordering = ["group__name"]

    def __str__(self) -> str:
        return f"MOTD for {self.group.name}"
