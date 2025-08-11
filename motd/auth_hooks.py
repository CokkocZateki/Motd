from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from . import urls
from .models import MotdMessage


class MotdMenuItemHook(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(
            self,
            'MOTD',
            'fas fa-bullhorn fa-fw',
            'motd:list',
            navactive=['motd:'],
        )

    def render(self, request):
        if request.user.has_perm('motd.view_motdmessage'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu():
    return MotdMenuItemHook()


@hooks.register('url_hook')
def register_url():
    return UrlHook(urls, 'motd', r'^motd/')


@hooks.register('dashboard_hook')
def register_dashboard(request):
    """Auto-inject dashboard widget"""
    if not request.user.has_perm('motd.view_motdmessage'):
        return ''

    active_messages = [
        message
        for message in MotdMessage.objects.filter(is_active=True)
        if message.can_user_see(request.user)
    ]

    priority_order = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1}
    active_messages.sort(
        key=lambda x: priority_order.get(x.priority, 0), reverse=True
    )

    context = {
        'messages': active_messages[:5],
        'user': request.user,
    }
    return render_to_string('motd/dashboard_widget.html', context, request=request)
