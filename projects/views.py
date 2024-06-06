from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def list_projects(request):
    return render(request, 'projects.html', {'active_page': 'projects'})

def new_project(request):
    return render(request, 'newproject.html', {'active_page': 'projects'})

def edit_project(request):
    return render(request, 'editproject.html', {'active_page': 'projects'})