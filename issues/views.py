from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from issues.forms import IssueForm, CommentForm
from issues.models import Issue, Comment, UserIssue
from projects.models import Project
from notifications.models import Change
from hitchhound.utils import paginate, get_new_notifications
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import F, Q
from django.utils import timezone
from django.core.exceptions import FieldError


@login_required
def list_issues(request):
    """
    View to list all issues, optionally filtered by project and sorted by various fields.
    Handles pagination and sorting, and includes user notifications.
    """
    # Retrieve and handle session flag for showing a success toast message when user just registered
    show_toast = request.session.pop('registration_success', False)
    
    # Get sorting and filtering parameters from the request
    sort_by = request.GET.get('sort_by', 'title')
    order = request.GET.get('order', 'asc')
    project_id = request.GET.get('project_id')

    project = None

    # Filter issues by project if project_id is provided
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        issues = Issue.objects.filter(project=project)
    else:
        issues = Issue.objects.all()

    # Determine the ordering of issues
    ordering = f'{'' if order == 'asc' else '-'}{sort_by.replace('.', '__')}'
    
    # Annotate and order issues based on sorting parameters
    if sort_by == 'title':
        issues = issues.annotate(lower_title=Lower('title')).order_by(f'{'' if order == 'asc' else '-'}lower_title')
    elif sort_by == 'project.title':
        issues = issues.annotate(project_title=Lower('project__title')).order_by(f'{'' if order == 'asc' else '-'}project_title')
    elif sort_by == 'severity':
        ordering = 'severity' if order == 'asc' else '-severity'
        issues = issues.order_by(ordering)
    else:
        try:
            issues = issues.order_by(ordering)
        except FieldError:
            issues = issues.order_by('title')  

    # Use the paginate utility function to handle pagination
    page_obj = paginate(request, issues)

    def toggle_order(current_order):
        """ 
        Utility function to toggle sorting order between ascending and descending.
        """
        return 'asc' if current_order == 'desc' else 'desc'

    # Calculate whether there are new notifications for the current user
    new_notifications = get_new_notifications(request.user)

    # Check if there's an alert type in the session and add it to the context
    alert_type = request.session.pop('Alert Type', None)

    context = {
        'active_page': 'issues',
        'show_toast': show_toast,
        'page_obj': page_obj,
        'project': project,
        'sort_by': sort_by,
        'order': order,
        'toggle_order': toggle_order(order),
        'new_notifications': new_notifications,
        'show_navbar': True,
        'alert_type': alert_type,
    }

    return render(request, 'issues.html', context)

@login_required
def issue_detail(request, id):
    """
    View to display the details of a specific issue, including its comments.
    """
    issue = get_object_or_404(Issue, id=id)
    comments = Comment.objects.filter(issue=issue).order_by('-commented_at')
    form = CommentForm()

    # Calculate whether there are new notifications for the current user
    new_notifications = get_new_notifications(request.user)

    context = {
        'issue': issue, 
        'comments': comments,
        'form': form, 
        'new_notifications': new_notifications,
        'active_page': 'issues',
        'show_navbar': True,
    }
    return render(request, 'issue_detail.html', context)

@login_required
def add_comment(request, issue_id):
    """ View to add a comment to a specific issue """
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.issue = issue
            comment.user = request.user
            comment.save()
            return redirect('issue_detail', id=issue.id)
    else:
        form = CommentForm()
    return render(request, 'issue_detail.html', {'issue': issue, 'form': form, 'comments': issue.comment_set.all()})

@login_required  
def create_issue(request):
    """ View to create a new issue """
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reporter = request.user
            issue.save()
            request.session['Alert Type'] = 'Issue Created'
            return redirect('issues')  
    else:
        form = IssueForm()
    
    # Calculate whether there are new notifications for the current user
    new_notifications = get_new_notifications(request.user)

    context = {
        'form': form, 
        'new_notifications': new_notifications,
        'active_page': 'issues',
        'show_navbar': True,
    }

    return render(request, 'create_issue.html', context)

@login_required
def edit_issue(request, id):
    """ View to edit an existing issue """
    issue = get_object_or_404(Issue, id=id)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            success = form.save(user=request.user)
            if not success:
                # Construct the message using display status names
                allowed_statuses = [dict(Issue.STATUS_CHOICES).get(status) for status in issue.get_allowed_statuses_for_role(request.user.role)]
                messages.error(
                    request, 
                    f'As a {request.user.role.replace("_", " ")}, you do not have permission to change the issue status to {issue.get_status_display()}. '
                    f'You may only change it to {", ".join(allowed_statuses)}.'
                )
            else:
                return redirect('issue_detail', id=issue.id)
    else:
        form = IssueForm(instance=issue)

    # Calculate whether there are new notifications for the current user
    new_notifications = get_new_notifications(request.user)

    context = {
        'form': form,
        'issue': issue,
        'new_notifications': new_notifications,
        'active_page': 'issues',
        'show_navbar': True,
    }
    return render(request, 'edit_issue.html', context)

@login_required
def delete_issue(request, id):
    """ View to delete an issue """
    issue = get_object_or_404(Issue, id=id)
    if request.method == 'POST':
        issue.delete()
        return redirect('issues')

    return redirect('issue_detail', id=id)
