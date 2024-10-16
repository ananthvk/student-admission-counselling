# Generated by Django 5.1.1 on 2024-09-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counselling', '0002_student_registration_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='college',
            name='college_type',
        ),
        migrations.RemoveField(
            model_name='college',
            name='contact_email',
        ),
        migrations.AddField(
            model_name='college',
            name='city',
            field=models.TextField(default='Location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='college',
            name='website',
            field=models.URLField(default='-'),
            preserve_default=False,
        ),
    ]
