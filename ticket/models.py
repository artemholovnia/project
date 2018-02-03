from django.db import models
from django.contrib.auth.models import User
from worker_registration.models import *
import os
from django.utils.timezone import datetime, now
from record.models import *
from django.contrib.auth import get_user
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver
from record.models import Record
import pathlib
from pralnia_project.settings import LOG_DIRS

DATE_FORMAT = '%d-%m-%Y'
TIME_FORMAT = '%H:%M'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, 'static/media/tickets_docs/error')

clear = '0'
STYCZEN = '1'
LUTY = '2'
MARZEC = '3'
KWIECIEN = '4'
MAJ = '5'
CZERWIEC = '6'
LIPIEC = '7'
SIERPIEN = '8'
WRZESIEN = '9'
PARZDZIERNIK = '10'
LISTOPAD = '11'
GRUDZIEN = '12'

class StatusForTicket(models.Model):
    title = models.CharField(max_length=16, blank=False, null=False, default='', verbose_name='status')
    short_title = models.CharField(max_length=2, blank=False, null=False, default='', verbose_name='short title')

    def __str__(self):
        return self.title

class StatusForCarpet(models.Model):
    title = models.CharField(max_length=16, blank=False, null=False, default='', verbose_name='status')
    short_title = models.CharField(max_length=2, blank=False, null=False, default='', verbose_name='short title')

    def __str__(self):
        return self.title

class Sale(models.Model):
    percent = models.SmallIntegerField(blank=False, default=0, verbose_name='percent')
    description = models.CharField(max_length=32, blank=False, null=True, default='', verbose_name='description')

    def __str__(self):
        return '%s - %s' % (self.percent, self.description)

    class Meta():
        ordering = ['-percent']

class Client(models.Model):
    name = models.CharField(max_length=16, blank=False, null=False, default='', verbose_name='client name')
    identificator = models.CharField(max_length=2, blank=False, null=False, default='', verbose_name='identificator')

    def __str__(self):
        return (self.name)

class Ticket(models.Model):
    monthes = (
        (STYCZEN, 'Styczeń'),
        (LUTY, 'Luty'),
        (MARZEC, 'Marzec'),
        (KWIECIEN, 'Kwiecień'),
        (MAJ, 'Maj'),
        (CZERWIEC, 'Czerwiec'),
        (LIPIEC, 'Lipiec'),
        (SIERPIEN, 'Sierpień'),
        (WRZESIEN, 'Wrzesień'),
        (PARZDZIERNIK, 'Parzdziernik'),
        (LISTOPAD, 'Listopad'),
        (GRUDZIEN, 'Grudzień'),
    )
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, verbose_name='client')
    worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING, verbose_name='created_by')
    identificator = models.CharField(max_length=8, blank=False, null=False, default='', verbose_name='identificator')
    ticket_number = models.CharField(max_length=8, blank=True, null=True, default='', verbose_name='ticket number')
    month = models.CharField(max_length=2, blank=False, null=False, choices=monthes, default=clear, verbose_name='month')
    phone_number = models.CharField(max_length=12, blank=False, null=False, default='',
                                    verbose_name='client phone number')
    address = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='address')
    carpets_nmb = models.SmallIntegerField(blank=True, null=True, default=0, verbose_name='carpets number')
    status = models.ForeignKey(StatusForTicket, on_delete=models.CASCADE, default=1,
                               verbose_name='status')
    created = models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name='created in')
    coast = models.FloatField(blank=True, null=True, default=0, verbose_name='ticket coast')
    is_express = models.BooleanField(blank=True, default=False, verbose_name='is express')
    is_ready = models.BooleanField(blank=True, default=False, verbose_name='is ready')
    #sale = models.ForeignKey(Sale, default=1, on_delete=models.DO_NOTHING, verbose_name='sale')
    attentions = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name='attentions')
    carpets_ready_nmb = models.SmallIntegerField(blank=True, default=0, verbose_name='carpets_ready_nmb')
    tags = models.CharField(max_length=1000, blank=True, null=True, default='', verbose_name='tags')

    def __str__(self):
        return 'Ticket %s created by %s in %s' % (self.ticket_number, self.worker, self.created)

    class Meta():
        ordering = ['-created']

    def save(self):
        #dodajemy tagi do (tags) w Ticket
        ticket_number = self.ticket_number.split('/')[0]
        month = self.ticket_number.split('/')[1]
        tags_list = [self.client.name, self.worker.user.username, self.identificator, self.phone_number, ticket_number, month]
        between = '-'
        tags_str = between.join(tags_list)
        self.tags = tags_str

        #poruwnujemy iłość dywanów z iłóścią gotowych dywanów. jezęli się zgadza, to zmieniamy (status) w Ticket na
        # 'gotowy'. jeżeli się nie zgadza, to zmieniamy status na 'nowy'
        if self.carpets_nmb == self.carpets_ready_nmb:
            self.status = StatusForTicket.objects.get(title='gotowy')
            self.is_ready = True
        else:
            self.status = StatusForTicket.objects.get(title='nowy')
            self.is_ready = False
        return super(Ticket, self).save()

#write ticket log
'''@receiver(post_delete, sender=Ticket)
def write_log(sender, instance, **kwargs):
    with open(os.path.join(BASE_DIR, 'static/app_log/ticket_logs/ticket.logs'), 'x') as log_file:
        log_file.write('ticket is deleted at %s on %s' % (now().time().strftime(TIME_FORMAT),
                                                          now().date().strftime(DATE_FORMAT)))
        log_file.close()'''

#delete ticket document
@receiver(post_delete, sender=Ticket)
def delete_ticket_document(sender, instance, **kwargs):
    try:
        ticket_saved = TicketSaved.objects.get(ticket_identificator=instance.identificator)
        os.remove(ticket_saved.path + ticket_saved.file_name)
        ticket_saved.delete()
    except TicketSaved.DoesNotExist:
        pass



class Carpet(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    height = models.FloatField(blank=True, null=True, default=0, verbose_name='height')
    width = models.FloatField(blank=True, null=True, default=0, verbose_name='width')
    status = models.ForeignKey(StatusForCarpet, on_delete=models.CASCADE, default=1,
                               verbose_name='status')
    neutralization = models.BooleanField(blank=True, default=False, verbose_name='neutralization')
    ozon = models.BooleanField(blank=True, default=False, verbose_name='ozon')
    impregnation = models.BooleanField(blank=True, default=False, verbose_name='impregnation')
    roztocz = models.BooleanField(blank=True, default=False, verbose_name='roztocz')
    siersc = models.BooleanField(blank=True, default=False, verbose_name='siersc')
    coast = models.FloatField(blank=True, null=True, default=0, verbose_name='carpet coast')

#create or update record
#zapisywanie lub aktualizacja record
@receiver(post_save, sender=Carpet)
def save_record(sender, instance, **kwargs):
    Record.objects.update_or_create(carpet=instance)
    record = Record.objects.get(carpet=instance)
    record.records += '/Status changed to " %s " at %s on %s' % (instance.status.short_title,
                                                                 record.updated.time().strftime(TIME_FORMAT),
                                                                 record.updated.date().strftime(DATE_FORMAT))
    record.save()

@receiver(pre_save, sender=Carpet)
def update_val_carpets_ready(sender, instance, **kwargs):
    carpet_status_before_saving = None
    try:
        carpet = Carpet.objects.get(id=instance.id)
        carpet_status_before_saving = carpet.status
        if carpet_status_before_saving == StatusForCarpet.objects.get(short_title='zw') \
                and instance.status != StatusForCarpet.objects.get(short_title='zw'):
            ticket = Ticket.objects.get(id=instance.ticket.id)
            ticket.carpets_ready_nmb -= 1
            ticket.save()
        if instance.status == StatusForCarpet.objects.get(short_title='zw'):
            ticket = Ticket.objects.get(id=instance.ticket.id)
            ticket.carpets_ready_nmb += 1
            ticket.save()
    except Carpet.DoesNotExist:
        pass
    
@receiver(pre_delete, sender=Carpet)
def delete_carpet(sender, instance, **kwargs):
    ticket = instance.ticket
    if instance.status == StatusForCarpet.objects.get(short_title='zw'):
        ticket.carpets_ready_nmb -= 1
        ticket.coast = 0
        ticket.save()
    else:
        ticket.coast = 0
        ticket.save()

######################################################################################################################
class Services(models.Model):
    per_m = models.SmallIntegerField(blank=False, null=False, default=0, verbose_name='per m')
    neutralization = models.SmallIntegerField(blank=False, null=False, verbose_name='neutralization')
    ozon = models.SmallIntegerField(blank=False, null=False, verbose_name='ozon')
    impregnation = models.SmallIntegerField(blank=False, null=False, verbose_name='impregnation')
    siersc = models.SmallIntegerField(blank=False, null=False, verbose_name='siersc')
    roztocz = models.SmallIntegerField(blank=False, null=False, verbose_name='roztocz')
    express = models.FloatField(blank=False, null=False, default=0, verbose_name='express')

class TicketSaved(models.Model):
    ticket_identificator = models.CharField(max_length=8, blank=False, null=False, default='')
    path = models.CharField(max_length=256, blank=False, null=False, default=PATH)
    file_name = models.CharField(max_length=32, blank=False, null=False, default='')




