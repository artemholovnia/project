# Generated by Django 2.0 on 2018-01-23 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worker_registration', '0003_worker_is_admin'),
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='worker',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='worker_registration.Worker'),
            preserve_default=False,
        ),
    ]