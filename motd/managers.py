# Django
from django.db import models

# Alliance Auth
from allianceauth.authentication.models import User
from allianceauth.services.hooks import get_extension_logger

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Motd
from motd import __title__

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


class MotdQuerySet(models.QuerySet):
    def visible_to(self, user: User):
        """Give all currently visible MOTDs for the user."""
        now = models.functions.Now()

        if user.is_superuser:
            logger.debug("Returning all motd for superuser %s.", user)
            return self
        try:
            char = user.profile.main_character
            assert char  # Main character must exist

            # 1. Public Motd
            q_public = models.Q(
                start_date__lte=now,
                restricted_to_states=None,
                restricted_to_groups=None,
            )
            # 2. Group-restricted Motd
            q_group = models.Q(
                start_date__lte=now,
                restricted_to_groups__in=user.groups.all(),
                restricted_to_states=None,
            )
            # 3. State-restricted Motd
            q_state = models.Q(
                start_date__lte=now,
                restricted_to_groups=None,
                restricted_to_states__in=[user.profile.state],
            )
            # 4. Group- and State-restricted Motd
            q_group_and_state = models.Q(
                start_date__lte=now,
                restricted_to_groups__in=user.groups.all(),
                restricted_to_states__in=[user.profile.state],
            )

            query = q_public | q_group | q_state | q_group_and_state
            return self.filter(query).distinct()
        except AssertionError:
            logger.debug("User %s has no main character. Nothing visible.", user)
            return self.none()


class MotdManagerBase(models.Manager):
    def get_queryset(self):
        return MotdQuerySet(self.model, using=self._db)

    def visible_to(self, user):
        return self.get_queryset().visible_to(user)


MotdManager = MotdManagerBase.from_queryset(MotdQuerySet)
