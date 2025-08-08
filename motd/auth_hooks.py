from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from django.utils.translation import gettext_lazy as _

from . import urls


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
