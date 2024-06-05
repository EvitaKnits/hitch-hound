from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def not_found(request):
    return HttpResponse("This is the 404 page")

def list_notifications(request):
    return HttpResponse("This is the notification list page")

def change_history(request):
    return HttpResponse("This is the change history page")