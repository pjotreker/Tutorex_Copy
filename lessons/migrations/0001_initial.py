# Generated by Django 3.2 on 2021-06-12 10:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom_id', models.CharField(max_length=40, unique=True)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=80)),
                ('age_range_min', models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('age_range_max', models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('time_frame_start', models.DateField(blank=True, default=None, null=True)),
                ('time_frame_end', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('hour', models.TimeField(blank=True, null=True)),
                ('subject', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=1000, null=True)),
                ('lesson_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LessonMaterials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='LessonTimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField()),
                ('duration', models.IntegerField(default=45)),
            ],
        ),
        migrations.CreateModel(
            name='StudentClassRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.classroom')),
            ],
        ),
    ]
