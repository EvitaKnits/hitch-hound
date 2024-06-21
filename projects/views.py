from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from projects.models import Project
from issues.models import Issue

# Create your views here.

def list_projects(request):
    projects = Project.objects.all()
    for project in projects:
        project.latest_issues = Issue.objects.filter(project_title=project).order_by('-created_at')[:3]

    return render(request, 'projects.html', {'projects': projects})

def view_all_issues(request, project_title):
    project = get_object_or_404(Project, title=project_title)
    issues = Issue.objects.filter(project_title=project).order_by('-created_at')
    return render(request, 'all_issues.html', {'project': project, 'issues': issues})

def create_project(request):
    return render(request, 'create_project.html')

def edit_project(request):
    return render(request, 'edit_project.html')