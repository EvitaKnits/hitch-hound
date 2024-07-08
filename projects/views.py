from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from projects.models import Project
from issues.models import Issue, UserIssue
from django.core.paginator import Paginator
from .forms import ProjectForm
from django.urls import reverse
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import F, Q
from notifications.models import Change
from django.utils import timezone

# Create your views here.

def list_projects(request):
    projects = Project.objects.all().order_by('title')
    for project in projects:
        project.latest_issues = Issue.objects.filter(project=project).order_by('-created_at')[:3]

    # Calculate new notifications
    current_user = request.user
    last_visited = current_user.last_visited_notifications or timezone.now()

    # Fetch issues the user is assigned to
    user_issues = UserIssue.objects.filter(user=current_user).values_list('issue', flat=True)

    # Fetch changes for issues the user is assigned to or where the user is the reporter, excluding changes made by the user
    changes = Change.objects.filter(
        Q(issue_id__in=user_issues) | Q(issue__reporter=current_user)
    ).exclude(user=current_user)

    # Determine if there are new notifications
    new_notifications = changes.filter(changed_at__gt=last_visited).exists()

    context = {
        'projects': projects,
        'new_notifications': new_notifications,
    }

    return render(request, 'projects.html', context)

def view_all_issues(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    issues = Issue.objects.filter(project=project)

    # Sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')

    # Determine the sorting field and annotation
    if sort_by == 'title':
        issues = issues.annotate(lower_title=Lower('title')).order_by(f"{'' if order == 'asc' else '-'}lower_title")
    else:
        issues = issues.order_by(f"{'' if order == 'asc' else '-'}{sort_by}")

    # Pagination
    paginator = Paginator(issues, 10)  # Show 10 issues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Toggle order for sorting links
    toggle_order = 'asc' if order == 'desc' else 'desc'

     # Calculate new notifications
    current_user = request.user
    last_visited = current_user.last_visited_notifications or timezone.now()

    # Fetch issues the user is assigned to
    user_issues = UserIssue.objects.filter(user=current_user).values_list('issue', flat=True)

    # Fetch changes for issues the user is assigned to or where the user is the reporter, excluding changes made by the user
    changes = Change.objects.filter(
        Q(issue_id__in=user_issues) | Q(issue__reporter=current_user)
    ).exclude(user=current_user)

    # Determine if there are new notifications
    new_notifications = changes.filter(changed_at__gt=last_visited).exists()

    context = {
        'project': project,
        'page_obj': page_obj,
        'sort_by': sort_by,
        'order': order,
        'toggle_order': toggle_order,
        'new_notifications': new_notifications,
    }
    return render(request, 'all_issues.html', context)

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects') 
    else:
        form = ProjectForm()

    # Calculate new notifications
    current_user = request.user
    last_visited = current_user.last_visited_notifications or timezone.now()

    # Fetch issues the user is assigned to
    user_issues = UserIssue.objects.filter(user=current_user).values_list('issue', flat=True)

    # Fetch changes for issues the user is assigned to or where the user is the reporter, excluding changes made by the user
    changes = Change.objects.filter(
        Q(issue_id__in=user_issues) | Q(issue__reporter=current_user)
    ).exclude(user=current_user)

    # Determine if there are new notifications
    new_notifications = changes.filter(changed_at__gt=last_visited).exists()

    context = {
        'form': form, 
        'new_notifications': new_notifications,
    }

    return render(request, 'create_project.html', context)

def edit_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    # Calculate new notifications
    current_user = request.user
    last_visited = current_user.last_visited_notifications or timezone.now()

    # Fetch issues the user is assigned to
    user_issues = UserIssue.objects.filter(user=current_user).values_list('issue', flat=True)

    # Fetch changes for issues the user is assigned to or where the user is the reporter, excluding changes made by the user
    changes = Change.objects.filter(
        Q(issue_id__in=user_issues) | Q(issue__reporter=current_user)
    ).exclude(user=current_user)

    # Determine if there are new notifications
    new_notifications = changes.filter(changed_at__gt=last_visited).exists()

    context = {
        'form': form, 
        'new_notifications': new_notifications,
    }
    return render(request, 'edit_project.html', context)

def delete_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully')
        return redirect('projects') 
    return redirect('project_detail', id=id)