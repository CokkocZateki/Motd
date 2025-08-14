from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import MotdMessage, GroupMotd, StateMotd


@admin.register(MotdMessage)
class MotdMessageAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'priority_display',
        'is_active',
        'start_date',
        'end_date',
        'show_to_all',
        'created_by',
        'status_display',
    ]
    list_filter = [
        'style',
        'is_active',
        'show_to_all',
        'created_at',
    ]
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    filter_horizontal = ['restricted_to_groups']

    fieldsets = [
        (
            'Message Content',
            {
                'fields': ['title', 'content', 'style'],
            },
        ),
        (
            'Display Settings',
            {
                'fields': ['is_active', 'start_date', 'end_date'],
            },
        ),
        (
            'Access Control',
            {
                'fields': ['show_to_all', 'restricted_to_groups'],
                'description': 'Show to all will display to users with Member state only',
            },
        ),
        (
            'Metadata',
            {
                'fields': ['created_by', 'created_at', 'updated_at'],
                'classes': ['collapse'],
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def priority_display(self, obj):
        colors = {
            'info': 'info',
            'success': 'success', 
            'warning': 'warning',
            'danger': 'danger'
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.style, 'secondary'),
            obj.get_style_display()
        )
    priority_display.short_description = 'Priority'

    def status_display(self, obj):
        if obj.is_currently_active():
            return format_html('<span style="color: green;">Active</span>')
        if not obj.is_active:
            return format_html('<span style="color: red;">Disabled</span>')
        if obj.start_date > timezone.now():
            return format_html('<span style="color: orange;">Scheduled</span>')
        if obj.end_date and obj.end_date <= timezone.now():
            return format_html('<span style="color: gray;">Expired</span>')
        return format_html('<span style="color: gray;">Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(GroupMotd)
class GroupMotdAdmin(admin.ModelAdmin):
    list_display = ("group", "enabled")
    list_filter = ("enabled",)
    search_fields = ("group__name",)


@admin.register(StateMotd)
class StateMotdAdmin(admin.ModelAdmin):
    list_display = ("state_name", "enabled")
    list_filter = ("enabled",)
    search_fields = ("state_name",)
