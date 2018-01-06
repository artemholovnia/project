from django.shortcuts import render, redirect
from django.contrib import auth

# Create your views here.

def login(request):
    dict = {}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'authentication/login.html', dict)
    else:
        return render(request, 'authentication/login.html', dict)

def logout(request):
    auth.logout(request)
    return redirect('/')
