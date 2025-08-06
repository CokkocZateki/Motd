from django.db import migrations, models
import django.db.models.deletion

from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(

            name='MotdMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the MOTD message', max_length=200)),
                ('content', models.TextField(help_text='Message content (HTML allowed)')),
                ('priority', models.CharField(choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('critical', 'Critical')], default='normal', help_text='Message priority level', max_length=10)),
                ('style', models.CharField(choices=[('info', 'Info (Blue)'), ('success', 'Success (Green)'), ('warning', 'Warning (Yellow)'), ('danger', 'Danger (Red)')], default='info', help_text='Bootstrap alert style', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, help_text='When this message should start displaying')),
                ('end_date', models.DateTimeField(blank=True, help_text='When this message should stop displaying (leave blank for permanent)', null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Whether this message is active')),
                ('show_to_all', models.BooleanField(default=True, help_text='Show to all authenticated users')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_motd_messages', to=settings.AUTH_USER_MODEL)),
                ('restricted_to_groups', models.ManyToManyField(blank=True, help_text='If specified, only show to users in these groups', to='auth.group')),
            ],
            options={
                'verbose_name': 'MOTD Message',
                'verbose_name_plural': 'MOTD Messages',
                'ordering': ['-priority', '-start_date'],
            name='GroupMotd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'verbose_name': 'Group MOTD',
                'verbose_name_plural': 'Group MOTDs',
                'ordering': ['group__name'],
            },
        ),
    ]
