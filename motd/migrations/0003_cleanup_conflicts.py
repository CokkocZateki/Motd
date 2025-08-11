from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration helps resolve conflicts between the two MOTD systems.
    Run this after fixing the code to clean up any inconsistencies.
    """

    dependencies = [
        ('motd', '0002_statemotd'),
    ]

    operations = []
