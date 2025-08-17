# Django
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

# AA Motd
from motd.models import MotdMessage


@admin.register(MotdMessage)
class MotdMessageAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "priority_display",
        "is_active",
        "start_date",
        "end_date",
        "created_by",
        "status_display",
    ]
    list_filter = [
        "style",
        "is_active",
        "created_at",
    ]
    search_fields = ["title", "content"]
    readonly_fields = ["created_at", "updated_at", "created_by"]
    filter_horizontal = ["restricted_to_groups", "restricted_to_states"]

    fieldsets = [
        (
            "Message Content",
            {
                "fields": ["title", "content", "style"],
            },
        ),
        (
            "Display Settings",
            {
                "fields": ["is_active", "start_date", "end_date"],
            },
        ),
        (
            "Access Control",
            {
                "fields": ["restricted_to_groups", "restricted_to_states"],
                "description": "Specify groups and states that can view this message.",
            },
        ),
        (
            "Metadata",
            {
                "fields": ["created_by", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Priority")
    def priority_display(self, obj):
        colors = {
            "info": "info",
            "success": "success",
            "warning": "warning",
            "danger": "danger",
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.style, "secondary"),
            obj.get_style_display(),
        )

    @admin.display(description="Status")
    def status_display(self, obj):
        now = timezone.now()
        # Scheduled: Startdatum liegt in der Zukunft
        if obj.start_date and obj.start_date > now:
            return format_html('<span style="color: orange;">Scheduled</span>')
        # Expired: Enddatum liegt in der Vergangenheit
        if obj.end_date and obj.end_date <= now:
            return format_html('<span style="color: gray;">Expired</span>')
        # Active: Jetzt zwischen Start und Enddatum (oder kein Enddatum) und aktiviert
        if (
            obj.is_active
            and obj.start_date <= now
            and (not obj.end_date or obj.end_date > now)
        ):
            return format_html('<span style="color: green;">Active</span>')
        # Disabled: Nicht aktiv, aber nicht abgelaufen
        if not obj.is_active:
            return format_html('<span style="color: red;">Disabled</span>')
        # Fallback
        return format_html('<span style="color: gray;">Inactive</span>')
