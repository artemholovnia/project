# Generated by Django 2.0 on 2018-01-16 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_ticketsaved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketsaved',
            name='ticket',
        ),
        migrations.AddField(
            model_name='ticketsaved',
            name='ticket_identificator',
            field=models.CharField(default='', max_length=8),
        ),
    ]
