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


class StateMotd(models.Model):
    """Stores a message of the day for a specific Alliance Auth state."""

    state_name = models.CharField(max_length=64, unique=True)
    message = models.TextField()
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "State MOTD"
        verbose_name_plural = "State MOTDs"
        ordering = ["state_name"]

    def __str__(self) -> str:
        return f"MOTD for state {self.state_name}"
