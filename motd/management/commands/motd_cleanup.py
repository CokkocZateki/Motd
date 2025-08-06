from django.core.management.base import BaseCommand
from django.utils import timezone

from motd.models import MotdMessage


class Command(BaseCommand):
    help = 'Clean up expired MOTD messages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deactivated without actually changing anything',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        now = timezone.now()

        expired_messages = MotdMessage.objects.filter(
            is_active=True,
            end_date__lt=now,
        )

        if dry_run:
            self.stdout.write(
                f"DRY RUN: Would deactivate {expired_messages.count()} expired messages"
            )
        else:
            expired_count = expired_messages.update(is_active=False)
            self.stdout.write(
                self.style.SUCCESS(f"Deactivated {expired_count} expired messages")
            )
