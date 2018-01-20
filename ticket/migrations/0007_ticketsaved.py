# Generated by Django 2.0 on 2018-01-16 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketSaved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(default='/home/artem/Python/pralnia_project/project/static/media/tickets_docs/error', max_length=256)),
                ('file_name', models.CharField(default='', max_length=32)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ticket.Ticket')),
            ],
        ),
    ]
