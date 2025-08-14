from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.utils import timezone


class MotdMessage(models.Model):
    """Model for storing MOTD messages"""

    STYLE_CHOICES = [
        ('info', 'Low Priority'),
        ('success', 'Medium Priority'),
        ('warning', 'High Priority'),
        ('danger', 'Important'),
    ]

    title = models.CharField(max_length=200, help_text="Title of the MOTD message")
    content = models.TextField(help_text="Message content (HTML allowed)")
    style = models.CharField(
        max_length=10,
        choices=STYLE_CHOICES,
        default='info',
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

    is_active = models.BooleanField(default=True, help_text="Whether this message is active")
    show_to_all = models.BooleanField(
        default=True,
        help_text="Show to all members (users with Member state)",
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
        related_name='created_motd_messages',
    )

    class Meta:
        ordering = ['-start_date']
        verbose_name = "MOTD Message"
        verbose_name_plural = "MOTD Messages"

    def __str__(self):
        return f"{self.title} ({self.get_style_display()})"

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")

    def is_currently_active(self):
        """Check if the message should be displayed right now"""
        if not self.is_active:
            return False

        now = timezone.now()
        if self.start_date > now:
            return False

        if self.end_date and self.end_date <= now:
            return False

        return True

    def can_user_see(self, user):
        """Check if a specific user can see this message"""
        if not self.is_currently_active():
            return False

        if self.show_to_all:
            # Only show to users with Member state
            if hasattr(user, 'profile') and hasattr(user.profile, 'state'):
                if user.profile.state.name == 'Member':
                    return True
            return False
# If show_to_all is False, check if user is in restricted groups
        if self.restricted_to_groups.exists():
            user_groups = user.groups.all()
            return self.restricted_to_groups.filter(id__in=user_groups.values_list('id', flat=True)).exists()

        return False


class GroupMotd(models.Model):
    """Stores a message of the day for a specific group."""
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
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
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    state_name = models.CharField(max_length=64, unique=True)
    message = models.TextField()
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "State MOTD"
        verbose_name_plural = "State MOTDs"
        ordering = ["state_name"]

    def __str__(self) -> str:
        return f"MOTD for state {self.state_name}"
