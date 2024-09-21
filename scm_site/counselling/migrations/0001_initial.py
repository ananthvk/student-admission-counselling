# Generated by Django 5.1.1 on 2024-09-21 22:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('contact_email', models.EmailField(max_length=254)),
                ('college_type', models.TextField()),
                ('code', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('code', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RankList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.TextField()),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_seats', models.PositiveIntegerField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselling.college')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselling.course')),
                ('ranklist', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='counselling.ranklist')),
            ],
        ),
        migrations.AddField(
            model_name='college',
            name='programs',
            field=models.ManyToManyField(through='counselling.Program', to='counselling.course'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RankListEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('ranklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselling.ranklist')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselling.student')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(default=0)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselling.program')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counselling.student')),
            ],
        ),
        migrations.AddConstraint(
            model_name='program',
            constraint=models.UniqueConstraint(fields=('college', 'course'), name='course_cannot_be_repeated_in_college'),
        ),
        migrations.AddConstraint(
            model_name='ranklistentry',
            constraint=models.UniqueConstraint(fields=('ranklist', 'student'), name='student_unique_in_ranklist'),
        ),
        migrations.AddConstraint(
            model_name='choiceentry',
            constraint=models.UniqueConstraint(fields=('student', 'program'), name='student_program_unique'),
        ),
    ]
