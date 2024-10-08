# Generated by Django 5.1.1 on 2024-10-08 17:47

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counselling', '0009_program_counselling_college_4aef51_idx_and_more'),
        ('preferences', '0003_alter_preferences_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitePreferences',
            fields=[
                ('preferences_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='preferences.preferences')),
                ('option_entry_enabled', models.BooleanField()),
            ],
            bases=('preferences.preferences',),
            managers=[
                ('singleton', django.db.models.manager.Manager()),
            ],
        ),
    ]
