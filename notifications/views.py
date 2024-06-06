from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def not_found(request):
    return render(request, 'notfound.html')

def list_notifications(request):
    return render(request, 'notifications.html')

def change_history(request):
    return render(request, 'changehistory.html')