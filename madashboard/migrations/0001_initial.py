from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
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
