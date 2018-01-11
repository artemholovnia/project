from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, FormView
from ticket.views import BaseView
from django.contrib import auth
from django.contrib.auth.models import User
from worker_registration.models import *
from .forms import *
from worker_registration.models import Worker

# Create your views here.

class CreateUser(BaseView, FormView):
    template_name = 'admin_site/create_user.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        if self.request.method == 'POST':
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            repeat_password = form.cleaned_data.get('repeat_password')
            try:
                get_user = User.objects.get(username=username)
            except User.DoesNotExist:
                User.objects.create_user(username=username, email='',password=password)
                return redirect(reverse('all_tickets'))
            return redirect(reverse('create_user'))

class CreateWorker(BaseView, CreateView):
    template_name = 'admin_site/create_worker.html'
    form_class = CreateWorkerForm

