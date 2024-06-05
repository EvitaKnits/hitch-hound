from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def list_projects(request):
    return HttpResponse("This is the project list page")

def new_project(request):
    return HttpResponse("This is the create a new project page")

def edit_project(request):
    return HttpResponse("This is the edit project page")