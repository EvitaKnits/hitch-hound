from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from notifications.models import Change
from issues.models import UserIssue
from django.db.models import Count
from issues.models import Issue
from projects.models import Project
from hitchhound.utils import paginate, get_new_notifications
from users.models import User


# Create your views here.

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
    
    # Use the paginate utility function
    page_obj = paginate(request, issues)

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)
    
    context = {
        'issues': page_obj,
        'status_choices': status_choices,
        'project_choices': project_choices,
        'selected_statuses': selected_statuses,
        'selected_project_ids': selected_project_ids,
        'page_obj': page_obj,
        'active_page': 'reports',
        'show_navbar': True,
        'new_notifications': new_notifications,
    }
    return render(request, 'issue_listing_by_status.html', context)

def issue_listing_by_assignee(request):
    selected_assignees = request.GET.getlist('assignee')
    include_unassigned = request.GET.get('include_unassigned', 'off') == 'on'
    
    issues = Issue.objects.all()
    
    if selected_assignees or include_unassigned:
        query = Q()
        if selected_assignees:
            for assignee in selected_assignees:
                query |= Q(developer__username=assignee) | Q(product_manager__username=assignee) | Q(quality_assurance__username=assignee)
        if include_unassigned:
            query |= Q(developer__isnull=True, product_manager__isnull=True, quality_assurance__isnull=True)
        issues = issues.filter(query).distinct()
    
    # Use the paginate utility function
    page_obj = paginate(request, issues)

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)

    user_choices = User.objects.all()
    
    context = {
        'issues': page_obj,
        'user_choices': user_choices,
        'selected_assignees': selected_assignees,
        'include_unassigned': include_unassigned,
        'page_obj': page_obj,
        'active_page': 'reports',
        'show_navbar': True,
        'new_notifications': new_notifications,
    }
    
    return render(request, 'issue_listing_by_assignee.html', context)

def issue_status_summary(request):
    selected_projects = request.GET.getlist('project')
    include_all = 'all' in selected_projects
    projects = Project.objects.all()
    
    if include_all or not selected_projects:
        issues = Issue.objects.all()
        selected_project_title = "All Projects"
    else:
        issues = Issue.objects.filter(project__id__in=selected_projects)
        selected_project_title = projects.get(id=selected_projects[0]).title if len(selected_projects) == 1 else "Multiple Projects"
    
    status_summary = issues.values('status').annotate(count=Count('status'))
    labels = [status['status'] for status in status_summary]
    data = [status['count'] for status in status_summary]

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)
    
    context = {
        'labels': labels,
        'data': data,
        'project_choices': projects,
        'selected_projects': selected_projects,
        'selected_project_title': selected_project_title,
        'active_page': 'reports',
        'show_navbar': True,
        'new_notifications': new_notifications,
    }
    
    return render(request, 'issue_status_summary.html', context)

def issue_severity_summary(request):
    selected_projects = request.GET.getlist('project')
    include_all = 'all' in selected_projects
    projects = Project.objects.all()
    
    if include_all or not selected_projects:
        issues = Issue.objects.all()
        selected_project_title = "All Projects"
    else:
        issues = Issue.objects.filter(project__id__in=selected_projects)
        selected_project_title = projects.get(id=selected_projects[0]).title if len(selected_projects) == 1 else "Multiple Projects"
    
    severity_summary = issues.values('severity').annotate(count=Count('severity'))
    labels = [severity['severity'] for severity in severity_summary]
    data = [severity['count'] for severity in severity_summary]

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)
    
    context = {
        'labels': labels,
        'data': data,
        'project_choices': projects,
        'selected_projects': selected_projects,
        'selected_project_title': selected_project_title,
        'active_page': 'reports',
        'show_navbar': True,
        'new_notifications': new_notifications,
    }
    
    return render(request, 'issue_severity_summary.html', context)
