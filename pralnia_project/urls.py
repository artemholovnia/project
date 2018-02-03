"""pralnia_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from access_permission.views import GetPermission

urlpatterns = [
    url(r'^$', GetPermission.as_view(), name='get_permission'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls'), name='api'),
    url(r'^ticket/', include('ticket.urls'), name='ticket'),
    url(r'^authentication/', include('authentication.urls'), name='authentication'),
    url(r'^admin_site/', include('admin_site.urls'), name='admin'),
    url(r'records/', include('record.urls'), name='records'),
]