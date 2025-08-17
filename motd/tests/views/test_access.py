"""TestView class."""

# Standard Library
from http import HTTPStatus
from unittest.mock import Mock, patch

# Django
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

# Alliance Auth (External Libs)
from app_utils.testing import create_user_from_evecharacter

# AA Motd
# AA MotD
from motd import views
from motd.models import MotdMessage
from motd.tests.testdata.generate_motd import create_motd
from motd.tests.testdata.load_allianceauth import load_allianceauth

INDEX_PATH = "motd.views"


class TestMotdAccess(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_allianceauth()

        cls.factory = RequestFactory()
        cls.user, cls.character_ownership = create_user_from_evecharacter(
            character_id=1001,
            permissions=[
                "motd.basic_access",
            ],
        )

        cls.user_manage, cls.character_ownership = create_user_from_evecharacter(
            character_id=1002,
            permissions=[
                "motd.basic_access",
                "motd.manage_access",
            ],
        )

        cls.motd_message = create_motd(
            user=cls.user,
            title="Test MOTD",
            content="This is a test message of the day.",
            style=MotdMessage.MessageType.INFO,
            start_date=timezone.now() - timezone.timedelta(days=1),
        )

    def test_dashboard_access(self):
        """Test dashboard access."""
        request = self.factory.get(reverse("motd:dashboard_widget"))
        request.user = self.user
        # when
        response = views.dashboard_widget(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Message of the Day")

    def test_motd_list(self):
        """Test MOTD list access."""
        # given
        request = self.factory.get(reverse("motd:list"))
        request.user = self.user

        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        # when
        response = views.motd_list(request)
        # then
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "This is a test message of the day.")
