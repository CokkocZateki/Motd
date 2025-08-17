# Standard Library
from unittest.mock import MagicMock

# Django
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

# Alliance Auth (External Libs)
from app_utils.testing import create_user_from_evecharacter

# AA Motd
from motd.auth_hooks import MotdDashboardItemHook, register_dashboard
from motd.tests.testdata.load_allianceauth import load_allianceauth


class TestAuthHooks(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_allianceauth()
        cls.factory = RequestFactory()
        cls.user_without_permission, cls.character_ownership = (
            create_user_from_evecharacter(character_id=1002)
        )
        cls.user_with_ma_permission, cls.character_ownership = (
            create_user_from_evecharacter(
                character_id=1001,
                permissions=["motd.basic_access"],
            )
        )

    def test_render_returns_widget_for_user_with_permission(self):
        # given
        request = self.factory.get("/")
        request.user = self.user_with_ma_permission
        rendered_item = MotdDashboardItemHook()

        # when
        response = rendered_item.render(request)
        # Convert SafeString to HttpResponse for testing
        response = HttpResponse(response)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<div id="motd-dashboard-widget" class="col-12 mb-3">',
            response.content.decode("utf-8"),
        )

    def test_register_motd_hook(self):
        # given
        hooks = register_dashboard()

        # then
        self.assertIsInstance(hooks, MotdDashboardItemHook)
