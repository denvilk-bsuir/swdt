# Generated by Django 5.1.3 on 2024-12-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_task_memory_limit_task_time_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='points',
            field=models.IntegerField(default=1),
        ),
    ]
