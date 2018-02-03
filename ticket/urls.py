from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^all/$', views.Tickets.as_view(), name='all_tickets'),
    url(r'^detail=(?P<ticket_identificator>\w+)/$', views.TicketDetail.as_view(), name='ticket_detail'),
    url(r'^calculate_ticket_coast=(?P<ticket_identificator>\w+)', views.calculate_ticket_coast, name='calculate_ticket_coast'),
    url(r'^create_ticket/$', views.TicketCreate.as_view(), name='create_ticket'),
    url(r'^delete_ticket=(?P<ticket_identificator>\w+)/$', views.delete_ticket, name='delete_ticket'),
    url(r'^delete_carpet/ticket=(?P<ticket_identificator>\w+)&id=(?P<carpet_id>\d+)/$', views.delete_carpet, name='delete_carpet'),
    url(r'^update_carpet/ticket=(?P<ticket_identificator>\w+)&id=(?P<carpet_id>\d+)/$', views.update_carpet, name='update_carpet'),
    url(r'^generate_ticket/ticket=(?P<ticket_identificator>\w+)/$', views.generate_ticket, name='generate_ticket'),

    url(r'^download_ticket/ticket=(?P<ticket_identificator>\w+)/$', views.download_ticket_document,
        name='download_ticket_document'),
    url(r'^delete_ticket_document/ticket=(?P<ticket_identificator>\w+)/$', views.delete_ticket_document,
        name='delete_ticket_document'),

    url(r'^filter=(?P<filtering_text>.+)/$', views.TicketsFiltering.as_view(), name='filtering_data'),

    url(r'^send_message/$', views.send_message, name='send_message'),
]