# Generated by Django 2.0 on 2018-01-23 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_record_worker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='worker',
        ),
    ]
