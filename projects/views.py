from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from projects.models import Project
from issues.models import Issue, UserIssue
from hitchhound.utils import paginate, get_new_notifications
from .forms import ProjectForm
from django.urls import reverse
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import F, Q
from notifications.models import Change
from django.utils import timezone

def list_projects(request):
    """ View to list all Projects, along with their 3 latest issues """
    projects = Project.objects.all().order_by('title')
    for project in projects:
        project.latest_issues = Issue.objects.filter(project=project).order_by('-created_at')[:3]

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)

    # Check if there's an alert type in the session and add it to the context
    alert_type = request.session.pop('Alert Type', None)

    context = {
        'projects': projects,
        'new_notifications': new_notifications,
        'active_page': 'projects',
        'show_navbar': True,
        'alert_type': alert_type,
    }

    return render(request, 'projects.html', context)

def view_all_issues(request, project_id):
    """ View to list all issues for a specific Project """
    project = get_object_or_404(Project, id=project_id)
    issues = Issue.objects.filter(project=project)

    # Sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')

    # Determine the sorting field and annotation
    if sort_by == 'title':
        issues = issues.annotate(lower_title=Lower('title')).order_by(f'{'' if order == 'asc' else '-'}lower_title')
    else:
        issues = issues.order_by(f'{'' if order == 'asc' else '-'}{sort_by}')

    # Use the paginate utility function for pagination
    page_obj = paginate(request, issues)

    # Toggle order for sorting links
    toggle_order = 'asc' if order == 'desc' else 'desc'

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)

    context = {
        'project': project,
        'page_obj': page_obj,
        'sort_by': sort_by,
        'order': order,
        'toggle_order': toggle_order,
        'new_notifications': new_notifications,
        'active_page': 'projects',
        'show_navbar': True,
    }
    return render(request, 'all_issues.html', context)

def create_project(request):
    """ View to create a new Project """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['Alert Type'] = 'Project Created'
            return redirect('projects') 
    else:
        form = ProjectForm()

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)

    context = {
        'form': form, 
        'new_notifications': new_notifications,
        'active_page': 'projects',
        'show_navbar': True,
    }

    return render(request, 'create_project.html', context)

def edit_project(request, id):
    """ View to edit an existing Project """
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)

    context = {
        'form': form, 
        'new_notifications': new_notifications,
        'active_page': 'projects',
        'show_navbar': True,
    }
    return render(request, 'edit_project.html', context)

def delete_project(request, id):
    """ View to delete a Project """
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully')
        return redirect('projects') 
    return redirect('project_detail', id=id)