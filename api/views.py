from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core import serializers
from .serializers import *
from ticket.models import *

from rest_framework.generics import ListAPIView
# Create your views here.

#/api/tickets/
def tickets(request):
    tickets = get_list_or_404(Ticket)
    serializer = TicketsSerializer(tickets, many=True)
    return JsonResponse(serializer.data, safe=False, status=301)

#/api/tickets/ticket_detail=(ticket_identificator)/
def ticket_detail(request, ticket_identificator):
    ticket = get_object_or_404(Ticket, identificator=ticket_identificator)
    serializer = TicketsSerializer(ticket)
    return JsonResponse(serializer.data, safe=False, status=301)

#/api/carpets/ticket_filtering=(ticket_identificator)/
def carpets_for_ticket(request, ticket_identificator):
    carpets = get_list_or_404(Carpet, ticket=get_object_or_404(Ticket, identificator=ticket_identificator))
    serializer = CarpetSerializer(carpets, many=True)
    return JsonResponse(serializer.data, safe=False, status=301)

#/api/carpets/carpet_detail=(carpet_id)/
def carpet_detail(request, carpet_id):
    carpet = get_object_or_404(Carpet, id=carpet_id)
    serializer = CarpetSerializer(carpet)
    return JsonResponse(serializer.data, safe=False, status=301)

#/api/carpets/update_carpet=(carpet_id)&change_status(short_status)/
    #short statuses:
        #wt - wytrzepany
        #wp - wyprany
        #zw - zwinięty
def change_carpet_status(request, carpet_id, short_title):
    if request.method == 'GET':
        carpet = Carpet.objects.get(id=carpet_id)
        carpet.status = StatusForCarpet.objects.get(short_title=short_title)
        carpet.save(update_fields='status')
        serializer = CarpetSerializer(carpet=get_object_or_404(Carpet, id=carpet_id))
        return JsonResponse(serializer.data, safe=False, status=301)
