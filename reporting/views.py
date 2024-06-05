from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def list_reports(request):
    return HttpResponse("This is the report list page")