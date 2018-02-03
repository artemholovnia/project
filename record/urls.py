from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^', Records.as_view(), name='record'),
]