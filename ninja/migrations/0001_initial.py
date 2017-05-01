# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-01 20:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Corequisites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_subject', models.CharField(max_length=20)),
                ('course_level', models.CharField(max_length=10)),
                ('course_title', models.CharField(max_length=200)),
                ('course_type', models.CharField(max_length=20)),
                ('course_units', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CoursesRecommended',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_recommended', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoursesTaken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_taken', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DPRfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='dprs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('question', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('answer', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InterchangeableCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_1', to='ninja.Course')),
                ('course_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_2', to='ninja.Course')),
            ],
        ),
        migrations.CreateModel(
            name='LastPDFUpdate',
            fields=[
                ('update_name', models.CharField(max_length=100)),
                ('last_update_time', models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('abbreviation', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MajorCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Course')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Major')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Course')),
                ('prerequisite_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prereq', to='ninja.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('class_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('section_number', models.CharField(max_length=10)),
                ('section_max_enrollment', models.IntegerField(default=0)),
                ('section_current_enrollment', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section', to='ninja.Course')),
            ],
        ),
        migrations.CreateModel(
            name='SectionSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(blank=True, max_length=20)),
                ('instructor', models.CharField(max_length=20)),
                ('days', models.CharField(max_length=10)),
                ('time_start', models.TimeField(blank=True, null=True)),
                ('time_end', models.TimeField(blank=True, null=True)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_schedule', to='ninja.Section')),
            ],
        ),
        migrations.CreateModel(
            name='SectionShortList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SectionStagedForRegistry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserFilters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_monday', models.BooleanField(default=True)),
                ('available_tuesday', models.BooleanField(default=True)),
                ('available_wednesday', models.BooleanField(default=True)),
                ('available_thursday', models.BooleanField(default=True)),
                ('available_friday', models.BooleanField(default=True)),
                ('available_saturday', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMajor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Major')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='interchangeablecourses',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Major'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('course_subject', 'course_level')]),
        ),
        migrations.AddField(
            model_name='corequisites',
            name='corequisite_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coreq', to='ninja.Course'),
        ),
        migrations.AddField(
            model_name='corequisites',
            name='main_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninja.Course'),
        ),
        migrations.AlterUniqueTogether(
            name='prerequisites',
            unique_together=set([('main_course', 'prerequisite_course')]),
        ),
    ]
