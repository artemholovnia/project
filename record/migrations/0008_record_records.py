# Generated by Django 2.0 on 2018-01-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0007_remove_record_carpet log'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='records',
            field=models.CharField(blank=True, default='', max_length=1600),
        ),
    ]
