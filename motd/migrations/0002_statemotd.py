from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateMotd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=200, unique=True)),
                ('message', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['state_name'],
                'verbose_name': 'State MOTD',
                'verbose_name_plural': 'State MOTDs',
                'ordering': ['state_name'],
            },
        ),
    ]
