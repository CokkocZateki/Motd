from django.contrib import admin
from .models import GroupMotd, StateMotd


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
