from django.shortcuts import render, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from .forms import OrderVerificationForm
from ticket.models import Ticket, StatusForTicket
from django.core import serializers

LOGIN_URL = '/authentication/login/'

class HomePage(TemplateView):
    template_name = 'home_page/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['user'] = get_user(self.request)
        context['order_verification_form'] = OrderVerificationForm
        return context

def ajax_order_verification(request):
    json_response = {}
    if request.method == 'POST' and request.is_ajax():
        order_number = request.POST['order_number']
        phone_number = request.POST['phone_number']
        try:
            tickets = Ticket.objects.filter(phone_number=phone_number)
            for ticket in tickets:
                if ticket.ticket_number.split('/')[0] == order_number:
                    json_response['is_existed'] = True
                    json_response['order_number'] = ticket.ticket_number
                    json_response['phone_number'] = ticket.phone_number
                    if ticket.status == get_object_or_404(StatusForTicket, short_title='gt') and ticket.coast != 0:
                        json_response['coast'] = ticket.coast
                    else:
                        json_response['status'] = ticket.status.title
            return JsonResponse(json_response)
        except Ticket.DoesNotExist:

            return HttpResponse(status=404)


