from django.shortcuts import render
from django.utils.timezone import datetime
from django.views.generic import ListView
from ticket.views import BaseView
from ticket.models import Carpet, StatusForCarpet
from django.shortcuts import get_list_or_404
from .models import *

# Create your views here.

class Records(BaseView, ListView):
    template_name = 'records/records.html'
    context_object_name = 'records'

    def get_queryset(self):
        self.object_list = get_list_or_404(Record, created=datetime.today())
        return self.object_list

    def get_context_data(self, **kwargs):
        context = super(Records, self).get_context_data(**kwargs)
        return context
