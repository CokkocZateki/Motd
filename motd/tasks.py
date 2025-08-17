"""App Tasks"""

# Third Party
from celery import shared_task

# Django
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

# Alliance Auth (External Libs)
from app_utils.logging import LoggerAddTag

# AA Motd
# AA Ledger
from motd import __title__, app_settings
from motd.models import MotdMessage

logger = LoggerAddTag(get_extension_logger(__name__), __title__)

MAX_RETRIES_DEFAULT = 3

# Default params for all tasks.
TASK_DEFAULTS = {
    "time_limit": app_settings.MOTD_TASKS_TIME_LIMIT,
    "max_retries": MAX_RETRIES_DEFAULT,
}

# Default params for tasks that need run once only.
TASK_DEFAULTS_ONCE = {**TASK_DEFAULTS, **{"base": QueueOnce}}


@shared_task(**TASK_DEFAULTS_ONCE)
def update_all_motd(runs=0):
    logger.debug("Updating all motd")
    now = timezone.now()

    expired_messages = MotdMessage.objects.filter(
        is_active=True,
        end_date__lt=now,
    )

    for message in expired_messages:
        message.is_active = False
        message.save()
        runs = runs + 1
    logger.info(_("Deactivated %d expired messages"), runs)

    return True
