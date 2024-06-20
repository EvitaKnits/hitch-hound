from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def list_projects(request):
    return render(request, 'projects.html', {'active_page': 'projects'})

def create_project(request):
    return render(request, 'create_project.html', {'active_page': 'projects'})

def edit_project(request):
    return render(request, 'edit_project.html', {'active_page': 'projects'})