from django.shortcuts import render
from django.http import HttpResponse
from projects.models import Project
from issues.models import Issue

# Create your views here.

def list_projects(request):
    projects = Project.objects.all()
    for project in projects:
        project.latest_issues = Issue.objects.filter(project_title=project).order_by('-created_at')[:3]

    return render(request, 'projects.html', {'projects': projects})

def create_project(request):
    return render(request, 'create_project.html')

def edit_project(request):
    return render(request, 'edit_project.html')