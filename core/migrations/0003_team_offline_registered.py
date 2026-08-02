# Generated manually for the offline-registration toggle feature

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_sponsor_sponsor_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='offline_registered',
            field=models.BooleanField(
                default=False,
                help_text='Ticked by an OC member once the team has physically checked in at the venue.',
            ),
        ),
    ]
