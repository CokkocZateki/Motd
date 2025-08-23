# Django
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls
from .models import MotdMessage


class MotdMenuItemHook(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(
            self,
            "MOTD",
            "fas fa-bullhorn fa-fw",
            "motd:list",
            navactive=["motd:"],
        )

    def render(self, request):
        if request.user.has_perm("motd.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return MotdMenuItemHook()


@hooks.register("url_hook")
def register_url():
    return UrlHook(urls, "motd", r"^motd/")


class MotdDashboardItemHook:
    def __init__(self):
        self.name = "MOTD Widget"
        self.order = 0  # CHANGED from 10 to 0 - will appear FIRST on dashboard

    def render(self, request):
        """Render the dashboard widget"""
        # pylint: disable=duplicate-code
        active_messages = MotdMessage.objects.visible_to(request.user).filter(
            is_active=True
        )[:5]

        # Pass permission check result to template
        context = {
            "messages": active_messages,
        }
        return render_to_string(
            "motd/dashboard_widget.html", context=context, request=request
        )


@hooks.register("dashboard_hook")
def register_dashboard():
    """Register the dashboard widget - returns a callable class instance"""
    return MotdDashboardItemHook()
