from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def user_login(request):
    return render(request, 'login.html')

def user_logout(request):
    return render(request, 'logout.html', {'active_page': 'logout'})

def user_signup(request):
    return render(request, 'signup.html')

def password_reset(request):
    return render(request, 'reset.html')

def user_profile(request):
    return render(request, 'profile.html', {'active_page': 'profile'})