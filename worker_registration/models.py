from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Position(models.Model):
    title = models.CharField(max_length=16, blank=False, null=False, default='default', verbose_name='Position')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created in')

    def __str__(self):
        return '%s' % (self.title)

class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created in')
    status = models.BooleanField(blank=True, default=1, verbose_name='status')
    permission = models.SmallIntegerField(blank=False, default=0, verbose_name='permission')

    def __str__(self):
        return '%s - %s' % (self.user.username, self.position.title)

