from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^tickets/', views.tickets, name='tickets'),
    url(r'^tickets/ticket_detail=(?P<ticket_identificator>\w+)/$', views.ticket_detail, name="ticket_detail"),
    url(r'^carpets/ticket_filtering=(?P<ticket_identificator>\w+)/$', views.carpets_for_ticket, name='carpets_for_ticket'),
    url(r'^carpets/carpet_detail=(?P<carpet_id>\d+)/$', views.carpet_detail, name='carpet_detail'),
    url(r'^carpets/update_carpet=(?P<carpet_id>\d+)&change_status=(?P<status_title>\w+)/$',
    views.change_carpet_status, name='change_carpet_status'),
]