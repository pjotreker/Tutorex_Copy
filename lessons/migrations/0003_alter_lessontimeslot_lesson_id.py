# Generated by Django 3.2 on 2021-06-09 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessontimeslot',
            name='lesson_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson'),
        ),
    ]
