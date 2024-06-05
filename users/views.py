from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def user_login(request):
    return HttpResponse("This is the login page")

def user_signup(request):
    return HttpResponse("This is the signup page")

def password_reset(request):
    return HttpResponse("This is the password reset page")

def user_profile(request):
    return HttpResponse("This is the user profile page")