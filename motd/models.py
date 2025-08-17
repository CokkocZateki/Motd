# Django
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.authentication.models import State

# AA Motd
from motd.managers import MotdManager


class General(models.Model):
    """A model defining commonly used properties and methods for Motd."""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access this app, Motd."),
            ("manage_access", "Can manage Motd."),
        )


class MotdMessage(models.Model):
    """Model for storing MOTD messages"""

    class MessageType(models.TextChoices):
        INFO = "info", _("Low Priority")
        SUCCESS = "success", _("Medium Priority")
        WARNING = "warning", _("High Priority")
        DANGER = "danger", _("Important")

        def bootstrap_icon_html(self):
            icon_map = {
                self.INFO: "info-circle",
                self.SUCCESS: "check-circle",
                self.WARNING: "exclamation-circle",
                self.DANGER: "exclamation-triangle",
            }
            icon_name = icon_map.get(self.value, "info-circle")
            return f'<i class="fas fa-{icon_name}"></i>'

    title = models.CharField(max_length=200, help_text="Title of the MOTD message")
    content = models.TextField(help_text="Message content (HTML allowed)")
    style = models.CharField(
        max_length=10,
        choices=MessageType.choices,
        default=MessageType.INFO,
        help_text="Message priority level",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(
        default=timezone.now,
        help_text="When this message should start displaying",
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this message should stop displaying (leave blank for permanent)",
    )

    is_active = models.BooleanField(
        default=True, help_text="Whether this message is active"
    )

    restricted_to_states = models.ManyToManyField(
        State,
        blank=True,
        help_text="If specified, only show to users in these states",
    )

    restricted_to_groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text="If specified, only show to users in these groups",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_motd_messages",
    )

    objects = MotdManager()

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "MOTD Message"
        verbose_name_plural = "MOTD Messages"
        default_permissions = ()

    def __str__(self):
        return f"{self.title} ({self.get_style_display()})"

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")
