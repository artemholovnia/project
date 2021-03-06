# Generated by Django 2.0 on 2018-01-01 21:15

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
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='default', max_length=16, verbose_name='Position')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created in')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created in')),
                ('status', models.BooleanField(default=1, verbose_name='status')),
                ('permission', models.SmallIntegerField(default=0, verbose_name='permission')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='worker_registration.Position')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
