from django.db import models
from django.contrib.auth.models import User
from worker_registration.models import *

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

    #sprawdzamy statusy dawanów w zlecenia. jeżeli dywan zmienił się status na 'zw', to dodajemy 1 do carpets_ready_nmb
    # w Ticket
    #jeżeli status dywanu się zmienił z zwiniętego na jaki kolwiekinny, to odejmujemy 1 od carpets_ready_nmb jeżeli jest
    #większe od 0
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.status == StatusForCarpet.objects.get(short_title='zw'):
            self.ticket.carpets_ready_nmb += 1
            self.ticket.save()
        else:
            if self.ticket.carpets_ready_nmb > 0:
                self.ticket.carpets_ready_nmb -= 1
            self.ticket.is_ready = False
            self.ticket.save()
        return super(Carpet, self).save()

    #jeżeli dywan został usunięty, to odejmujemy 1 z carpets_ready_nmb w Ticket
    def delete(self, using=None, keep_parents=False):
        self.ticket.carpets_ready_nmb -= 1
        self.ticket.coast = 0
        self.ticket.save()
        return super(Carpet, self).delete()



