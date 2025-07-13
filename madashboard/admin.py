from django.contrib import admin
from .models import GroupMotd


@admin.register(GroupMotd)
class GroupMotdAdmin(admin.ModelAdmin):
    list_display = ("group", "enabled")
    list_filter = ("enabled",)
    search_fields = ("group__name",)
