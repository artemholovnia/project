# Generated by Django 2.0 on 2018-01-09 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker_registration', '0002_auto_20180109_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='is admin'),
        ),
    ]
