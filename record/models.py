from django.db import models
from django.utils.timezone import datetime
from django.utils.timezone import now

# Create your models here.

TIME_FORMAT = '%H:%m'
DATE_FORMAT = '%d-%m-%Y'

class Record(models.Model):
    carpet = models.OneToOneField('ticket.Carpet', on_delete=models.CASCADE, name='carpet')
    created = models.DateField(blank=False, null=False, auto_now_add=True, name='created')
    updated = models.DateTimeField(blank=False, null=False, auto_now=True, name='updated')
    records = models.CharField(max_length=1600, blank=True, null=False, default='', name='records')

    '''def save(self):
        self.logs += '/Status dawanu zostal zmieniony na %s w godzinie %s %s' % (self.carpet.status.title,
                            self.updated.date().strftime(DATE_FORMAT), self.updated.time().strftime(TIME_FORMAT))
        return super(Record, self).save()'''

