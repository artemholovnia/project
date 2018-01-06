from django.shortcuts import render
from django.contrib.auth import get_user
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ticket.models import Worker

LOGIN_URL = '/authentication/login/'

@method_decorator(login_required(login_url=LOGIN_URL), name='dispatch')
class GetPermission(TemplateView):
    template_name = 'access_permission/get_permission.html'

    def get_context_data(self, **kwargs):
        context = super(GetPermission, self).get_context_data(**kwargs)
        try:
            user_permission = Worker.objects.get(user_id=get_user(self.request).id).permission
        except Worker.DoesNotExist:
            user_permission = 0
        context['user_permission'] = user_permission
        if user_permission == 0:
            context['redirect_url'] = reverse('all_tickets')
        return context
