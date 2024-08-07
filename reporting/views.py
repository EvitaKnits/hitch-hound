from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from issues.models import Issue
from projects.models import Project
from hitchhound.utils import paginate, get_new_notifications
from users.models import User


@login_required
def issue_listing_by_status(request):
    """
    View to list issues filtered by their status and project.
    """
    # Retrieve status choices and all projects
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

    # Use the paginate utility function to handle pagination
    page_obj = paginate(request, issues)

    context = {
        'issues': page_obj,
        'status_choices': status_choices,
        'project_choices': project_choices,
        'selected_statuses': selected_statuses,
        'selected_project_ids': selected_project_ids,
        'page_obj': page_obj,
        'active_page': 'reports',
        'show_navbar': True,
        'new_notifications': get_new_notifications(request.user),
    }
    return render(request, 'issue_listing_by_status.html', context)


@login_required
def issue_listing_by_assignee(request):
    """ View to list issues filtered by their assignee """
    # Get selected assignees and if including unassigned issues from request
    selected_assignees = request.GET.getlist('assignee')
    include_unassigned = request.GET.get('include_unassigned', 'off') == 'on'

    # Start with all issues
    issues = Issue.objects.all()

    if selected_assignees or include_unassigned:
        query = Q()

        if selected_assignees:
            for assignee in selected_assignees:
                query |= (
                    Q(developer__username=assignee) |
                    Q(product_manager__username=assignee) |
                    Q(quality_assurance__username=assignee)
                )

        if include_unassigned:
            query |= Q(
                developer__isnull=True,
                product_manager__isnull=True,
                quality_assurance__isnull=True
            )

        issues = issues.filter(query).distinct()

    # Use the paginate utility function to handle pagination
    page_obj = paginate(request, issues)

    user_choices = User.objects.all()

    context = {
        'issues': page_obj,
        'user_choices': user_choices,
        'selected_assignees': selected_assignees,
        'include_unassigned': include_unassigned,
        'page_obj': page_obj,
        'active_page': 'reports',
        'show_navbar': True,
        'new_notifications': get_new_notifications(request.user),
    }

    return render(request, 'issue_listing_by_assignee.html', context)


@login_required
def issue_status_summary(request):
    """ View to display a summary of issue statuses by project """
    # Get selected projects from the request
    selected_projects = request.GET.getlist('project')
    include_all = 'all' in selected_projects
    projects = Project.objects.all()

    # Determine which issues to include based on selected projects
    if include_all or not selected_projects:
        issues = Issue.objects.all()
        selected_project_title = 'All Projects'
    else:
        issues = Issue.objects.filter(project__id__in=selected_projects)
        selected_project_title = (
            projects.get(id=selected_projects[0]).title
            if len(selected_projects) == 1
            else 'Multiple Projects'
        )

    # Summarise issues by status
    status_summary = issues.values('status').annotate(count=Count('status'))

    # Map status values to their display names
    status_dict = dict(Issue.STATUS_CHOICES)
    labels = [status_dict[status['status']] for status in status_summary]
    data = [status['count'] for status in status_summary]

    context = {
        'labels': labels,
        'data': data,
        'project_choices': projects,
        'selected_projects': selected_projects,
        'selected_project_title': selected_project_title,
        'active_page': 'reports',
        'show_navbar': True,
        'new_notifications': get_new_notifications(request.user),
    }

    return render(request, 'issue_status_summary.html', context)


@login_required
def issue_severity_summary(request):
    """ View to display a summary of issue severities by project """
    # Get selected projects from the request
    selected_projects = request.GET.getlist('project')
    include_all = 'all' in selected_projects
    projects = Project.objects.all()

    # Determine which issues to include based on selected projects
    if include_all or not selected_projects:
        issues = Issue.objects.all()
        selected_project_title = 'All Projects'
    else:
        issues = Issue.objects.filter(project__id__in=selected_projects)
        selected_project_title = (
           projects.get(id=selected_projects[0]).title
           if len(selected_projects) == 1
           else 'Multiple Projects'
        )

    # Summarise issues by severity
    severity_summary = (
        issues.values('severity').annotate(count=Count('severity'))
    )
    severity_mapping = dict(Issue.SEVERITY_CHOICES)
    labels = [
        severity_mapping[severity['severity']]
        for severity in severity_summary
    ]
    data = [severity['count'] for severity in severity_summary]

    context = {
        'labels': labels,
        'data': data,
        'project_choices': projects,
        'selected_projects': selected_projects,
        'selected_project_title': selected_project_title,
        'active_page': 'reports',
        'show_navbar': True,
        'new_notifications': get_new_notifications(request.user),
    }

    return render(request, 'issue_severity_summary.html', context)
