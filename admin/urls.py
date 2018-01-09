from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create_user/$', CreateUser.as_view(), name='create_user'),
    url(r'^create_worker/$', CreateWorker.as_view(), name='create_worker'),

]
