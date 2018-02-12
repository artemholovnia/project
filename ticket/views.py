from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import FormView, UpdateView
from django.contrib import auth
from .models import *
from worker_registration.models import *
from .generate_ticket import generate_ticket_document
from django.shortcuts import get_list_or_404, get_object_or_404
from .forms import *
from django.utils.timezone import datetime
from django.urls import reverse
import string
import random
import os
#from twilio.rest import Client as ClientMessage

DATE_FORMAT = '%d-%m-%Y'
TIME_FORMAT = '%H:%M'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, 'static/media/tickets_docs/' + datetime.today().strftime(DATE_FORMAT))

services = Services.objects.get(id=1)
COAST_PER_M = services.per_m
COAST_N = services.neutralization
COAST_I = services.impregnation
COAST_O = services.ozon
COAST_R = services.roztocz
COAST_S = services.siersc
COAST_EXSPRESS = services.express

LOGIN_URL = '/authentication/login/'
IDENTIFICATOR_FOR_TICKET = 8

#Создание идентификатора по длинне
def create_identificator(len):
    identificator_join = ''
    identificator_dict = []
    for sym in range(len):
        identificator_sym = random.choice(string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase)
        identificator_dict.append(identificator_sym)
    identificator = identificator_join.join(identificator_dict)
    return identificator

#Функция подсчета уже измерянных ковров
def get_carpets_nmb(ticket_identificator):
    ticket = get_object_or_404(Ticket, identificator=ticket_identificator).id
    carpets_nmb = len(Carpet.objects.filter(ticket_id=ticket))
    return carpets_nmb

#Базовый класс с набором стандартного context data для всех представлений
@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class BaseView(View):

#app_name - название приложения
#active_tickets - объекты всех существующий активных квитанций
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        try:
            worker = Worker.objects.get(user=auth.get_user(self.request))
        except Worker.DoesNotExist:
            worker = False
        context['worker'] = worker
        context['app_name'] = 'ticket'
        context['date_today'] = datetime.today().strftime(DATE_FORMAT)
        return context

#Представление всех квитанций
@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class Tickets(BaseView, ListView):
    model = Ticket
    template_name = 'ticket/ticket_list.html'
    context_object_name = 'tickets'

#Нужно явно определить self.objects_list для того, чтоб можно было наследовать эллементы TemplateView.
#get_queryset() берет объекты из model через метод default_manager.all(). Так же можно явно указать queryset
#чтоб не вызывать метод get_queryset(), но все равно придется обределить переменную self.objects_list = self.queryset
    def get_ordering(self):
        self.ordering = ['-created']
        return super(Tickets, self).get_ordering()

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset() #c этой строкой работает второй класс BaseView
        return super(Tickets, self).get_context_data(**kwargs)

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class TicketsFiltering(BaseView, ListView):
    template_name = 'ticket/ticket_list.html'
    context_object_name = 'tickets'
    
    def get_ordering(self):
        self.ordering = ['-created']
        return super(TicketsFiltering, self).get_ordering()

    def get_queryset(self):
        self.object_list = []
        kwargs = self.kwargs.get('filtering_text')
        kwargs_list = kwargs.split('&')
        tickets = get_list_or_404(Ticket)
        for kwarg in kwargs_list:
            for ticket in tickets:
                tags_list = ticket.tags.split('-')
                for tag in tags_list:
                    if kwarg == tag:
                        if ticket not in self.object_list:
                            self.object_list.append(ticket)
        return self.object_list

    def get_context_data(self, **kwargs):
        return super(TicketsFiltering, self).get_context_data(**kwargs)

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class TicketDetail(BaseView, DetailView, FormView):
    model = Ticket
    form_class = CarpetCreateForm
    template_name = 'ticket/ticket_detail.html'
    slug_url_kwarg = 'ticket_identificator'
    slug_field = 'identificator'

    def get_success_url(self):
        identificator = self.kwargs.get(self.slug_url_kwarg)
        success_url = reverse('ticket_detail', args=[identificator])
        return success_url

    def form_valid(self, form):
        self.object = self.get_object()
        carpet = form.save(commit=False)
        carpet.ticket = Ticket.objects.get(identificator=self.object.identificator)
        carpet.status = StatusForCarpet.objects.get(title='wytrzepany')
        carpet.save()
        return super(TicketDetail, self).form_valid(form)

#self.object - переменная в которой хранится объект представление (Carpet.object.get(slug_field=slug_url_kwarg))
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(TicketDetail, self).get_context_data(**kwargs)
        context['carpet_update_form'] = CarpetUpdateForm
        context['carpets_ready'] = Carpet.objects.filter(ticket_id=self.object.id)
        context['carpets_nmb'] = self.object.carpets_nmb - get_carpets_nmb(self.object.identificator)
        try:
            is_saved = TicketSaved.objects.get(ticket_identificator=self.object.identificator)
            context['is_saved'] = True
            context['saved_ticket_file_name'] = is_saved.file_name[1:]
        except TicketSaved.DoesNotExist:
            context['is_saved'] = False

        return context

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class TicketCreate(BaseView, FormView):
    template_name = 'ticket/create_ticket.html'
    form_class = TicketCreateForm

    def get_context_data(self, **kwargs):
        last_ticket_number_for_transport = 0
        last_ticket_number_for_personal = 0

        try:
            transport_tickets = Ticket.objects.filter(client=Client.objects.get(name='Transport'))
        except Ticket.DoesNotExist:
            transport_tickets = None

        try:
            personal_tickets = Ticket.objects.filter(client=Client.objects.get(name='Osobisty'))
        except Ticket.DoesNotExist:
            personal_tickets = None

        #Receive the latest created number of ticket for Transport
        if transport_tickets is not None:
            for ticket in transport_tickets:
                first_symbol = int(ticket.ticket_number.split('/')[0])
                if first_symbol > last_ticket_number_for_transport:
                    last_ticket_number_for_transport = first_symbol

        # Receive the latest created number of ticket for Personal
        if personal_tickets is not None:
            for ticket in personal_tickets:
                first_symbol = int(ticket.ticket_number.split('/')[0])
                if first_symbol > last_ticket_number_for_personal:
                    last_ticket_number_for_personal = first_symbol
        context = super(TicketCreate, self).get_context_data(**kwargs)
        context['last_ticket_number_for_transport'] = last_ticket_number_for_transport
        context['last_ticket_number_for_personal'] = last_ticket_number_for_personal
        context['month_for_select'] = datetime.today().month
        return context

    def form_valid(self, form):
        identificator = create_identificator(IDENTIFICATOR_FOR_TICKET)
        month = form.cleaned_data['month']
        ticket_number = form.cleaned_data['ticket_number']
        ticket = form.save(commit=False)
        ticket.ticket_number = ticket_number + '/' + month
        try:
            ticket.worker = Worker.objects.get(user_id=auth.get_user(self.request).id)
        except Worker.DoesNotExist:
            return redirect(reverse('create_ticket'))
        ticket.status = StatusForTicket.objects.only('id').get(title='nowy')
        ticket.identificator = identificator
        ticket.save()
        self.success_url = '/ticket/detail=' + identificator + '/'
        return redirect(self.success_url)

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class EditTicket(BaseView, UpdateView):
    model = Ticket
    template_name = 'ticket/create_ticket.html'
    fields = ('__all__')
    slug_field = 'identificator'
    slug_url_kwarg = 'ticket_identificator'


#wyliczenie ceny zlecenia
@login_required(login_url=LOGIN_URL)
def calculate_ticket_coast(request, ticket_identificator):
    if request.method == 'GET':
        ticket = get_object_or_404(Ticket, identificator=ticket_identificator)
        carpets = get_list_or_404(Carpet, ticket=ticket)
        ticket_coast = 0
        carpets_coastes = []
        for carpet in carpets:
            per_m = COAST_PER_M
            if ticket.is_express:
                per_m *= COAST_EXSPRESS
            print(per_m)
            coast = 0
            carpet_size = carpet.height * carpet.width
            if carpet.neutralization:
                per_m += COAST_N
            if carpet.impregnation:
                per_m += COAST_I
            if carpet.ozon:
                coast += COAST_O
            if carpet.roztocz:
                per_m += COAST_R
            if carpet.siersc:
                per_m += COAST_S
            coast += carpet_size * per_m
            carpet.coast = coast
            carpet.save()
            carpets_coastes.append(coast)
        for carpet_coast in carpets_coastes:
            ticket_coast += carpet_coast
        ticket.coast = ticket_coast
        ticket.save()
    return redirect(reverse('ticket_detail', args=[ticket_identificator]))

@login_required(login_url=LOGIN_URL)
def delete_ticket(request, ticket_identificator):
    ticket = get_object_or_404(Ticket, identificator=ticket_identificator)
    ticket.delete()
    return redirect(reverse('all_tickets'))

@login_required(login_url=LOGIN_URL)
def delete_carpet(request, ticket_identificator, carpet_id):
    carpet = get_object_or_404(Carpet, id=carpet_id)
    carpet.delete()
    return redirect(reverse('ticket_detail', args=[ticket_identificator]))

@login_required(login_url=LOGIN_URL)
def update_carpet(request, ticket_identificator, carpet_id):
    try:
        carpet = Carpet.objects.get(id=carpet_id)
    except Carpet.DoesNotExist:
        return reverse('ticket_detail', args=[ticket_identificator])

    if request.method == 'POST':
        form = CarpetUpdateForm(request.POST)
        update_fields = []
        if form.is_valid():
            height = form.cleaned_data['height']
            width = form.cleaned_data['width']
            status = form.cleaned_data['status']
            neutralization = form.cleaned_data['neutralization']
            ozon = form.cleaned_data['ozon']
            impregnation = form.cleaned_data['impregnation']
            siersc = form.cleaned_data['siersc']
            roztocz = form.cleaned_data['roztocz']
            if height != carpet.height:
                carpet.height = height
                update_fields.append('height')
            if width != carpet.width:
                carpet.width = width
                update_fields.append('width')
            if status != carpet.status:
                carpet.status = status
                update_fields.append('status')
            if neutralization != carpet.neutralization:
                carpet.neutralization = neutralization
                update_fields.append('neutralization')
            if impregnation != carpet.impregnation:
                carpet.impregnation = impregnation
                update_fields.append('impregnation')
            if ozon != carpet.ozon:
                carpet.ozon = ozon
                update_fields.append('ozon')
            if siersc != carpet.siersc:
                carpet.siersc = siersc
                update_fields.append('siersc')
            if roztocz != carpet.roztocz:
                carpet.roztocz = roztocz
                update_fields.append('roztocz')
            carpet.save(update_fields=update_fields)
            return redirect(reverse('ticket_detail', args=[ticket_identificator]))

@login_required(login_url=LOGIN_URL)
def change_status(request, ticket_identificator, carpet_id, short_title):
    if request.method == 'GET':
        carpet = Carpet.objects.get(id=carpet_id)
        carpet.status = StatusForCarpet.objects.get(short_title=short_title)
        carpet.save(update_fields='status')
        return redirect(reverse('ticket_detail', args=[ticket_identificator]))

#####################
#DOCUMENT

#generate tikcet
#@login_required(login_url=LOGIN_URL)
def generate_ticket(request, ticket_identificator):
    if request.method == 'GET':
        generate_ticket_document(ticket_identificator)
        return redirect(reverse('ticket_detail', args=[ticket_identificator]))

#pobieranie kwitu
@login_required(login_url=LOGIN_URL)
def download_ticket_document(request, ticket_identificator):
    download_ticket = get_object_or_404(TicketSaved, ticket_identificator=ticket_identificator)
    if request.method == 'GET':
        with open(download_ticket.path + download_ticket.file_name, 'rb') as file:
            response= HttpResponse(file.read(), content_type='application/xls')
            response['Content-Disposition'] = 'inline; filename=' + download_ticket.file_name
            return response

#usunięncie kwitu z servera
@login_required(login_url=LOGIN_URL)
def delete_ticket_document(request, ticket_identificator):
    deleted_ticket = get_object_or_404(TicketSaved, ticket_identificator=ticket_identificator)
    if request.method == 'GET':
        os.remove(deleted_ticket.path + deleted_ticket.file_name)
        deleted_ticket.delete()
        return redirect(reverse('ticket_detail', args=[ticket_identificator]))

def send_message(request):

    # Your Account SID from twilio.com/console
    account_sid = 'AC4f7e8463b6cf70399fb760cafd5e8f27'
    # Your Auth Token from twilio.com/console
    auth_token = '8ebfdc7f9f88284a3073ce0982d92e3c'

    client = ClientMessage(account_sid, auth_token)

    message = client.messages.create(
        to="+48535806491",
        from_="+48814784651",
        body="Hello from Python!")

    print(message.sid)