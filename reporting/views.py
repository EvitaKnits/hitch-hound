from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from notifications.models import Change
from issues.models import UserIssue
from django.db.models import Count
from issues.models import Issue
from projects.models import Project


# Create your views here.

def list_reports(request):

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
        'new_notifications': new_notifications,
    }

    return render(request, 'reports.html', context)

def issue_listing_by_status(request):
    status_choices = Issue.STATUS_CHOICES
    project_choices = Project.objects.all()
    
    # Get selected statuses and projects from the request
    selected_statuses = request.GET.getlist('status')
    selected_project_ids = request.GET.getlist('project_id')
    
    # Filter issues based on the selected statuses and projects
    issues = Issue.objects.all()
    
    if selected_statuses:
        issues = issues.filter(status__in=selected_statuses)
    
    if selected_project_ids:
        issues = issues.filter(project_id__in=selected_project_ids)
    
    context = {
        'issues': issues,
        'status_choices': status_choices,
        'project_choices': project_choices,
        'selected_statuses': selected_statuses,
        'selected_project_ids': selected_project_ids,
    }
    return render(request, 'issue_listing_by_status.html', context)