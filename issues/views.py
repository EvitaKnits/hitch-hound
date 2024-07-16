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

# Create your views here.

@login_required
def list_issues(request):
    show_toast = request.session.pop('registration_success', False)
    sort_by = request.GET.get('sort_by', 'title')
    order = request.GET.get('order', 'asc')
    project_id = request.GET.get('project_id')

    project = None

    if project_id:
        project = get_object_or_404(Project, id=project_id)
        issues = Issue.objects.filter(project=project)
    else:
        issues = Issue.objects.all()

    # Determine the ordering
    ordering = f"{'' if order == 'asc' else '-'}{sort_by.replace('.', '__')}"
    
    if sort_by == 'title':
        issues = issues.annotate(lower_title=Lower('title')).order_by(f"{'' if order == 'asc' else '-'}lower_title")
    elif sort_by == 'project.title':
        issues = issues.annotate(project_title=Lower('project__title')).order_by(f"{'' if order == 'asc' else '-'}project_title")
    else:
        try:
            issues = issues.order_by(ordering)
        except FieldError:
            issues = issues.order_by('title')  # fallback to default ordering if invalid field

    # Use the paginate utility function
    page_obj = paginate(request, issues)

    def toggle_order(current_order):
        return 'asc' if current_order == 'desc' else 'desc'

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)

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
    }

    return render(request, 'issues.html', context)

@login_required
def issue_detail(request, id):
    issue = get_object_or_404(Issue, id=id)
    comments = Comment.objects.filter(issue=issue).order_by('-commented_at')
    form = CommentForm()

    # Calculate new notifications
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
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reporter = request.user
            issue.save()
            return redirect('issues')  
    else:
        form = IssueForm()
    
    # Calculate new notifications
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
    issue = get_object_or_404(Issue, id=id)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            success = form.save(user=request.user)  # Pass the user to the save method
            if not success:
                messages.error(
                    request, 
                    f"As a {request.user.role.replace('_', ' ')}, you do not have permission to change the issue status to {issue.status}. "
                    f"You may only change it to {', '.join(issue.get_allowed_statuses_for_role(request.user.role))}."
                )
            else:
                return redirect('issue_detail', id=issue.id)
    else:
        form = IssueForm(instance=issue)

    # Calculate new notifications
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
def change_issue_status(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        user_role = request.user.role
        allowed_statuses = issue.get_allowed_statuses_for_role(user_role)

        if issue.can_user_update_status(request.user, new_status):
            issue.status = new_status
            issue.save(user=request.user)
            return redirect('issue_detail', pk=pk)
        else:
            request.session['alert_message'] = (
                f"As a {user_role.replace('_', ' ')}, you do not have permission to change the issue status to {new_status}. "
                f"You may only change it to {', '.join(allowed_statuses)}."
            )
            request.session['alert_type'] = 'danger'
            return redirect('issue_detail', pk=pk)
    return render(request, 'issues/change_status.html', {'issue': issue})

@login_required
def delete_issue(request, id):
    issue = get_object_or_404(Issue, id=id)
    if request.method == 'POST':
        issue.delete()
        return redirect('issues')

    return redirect('issue_detail', id=id)
