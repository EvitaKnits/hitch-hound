from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from issues.forms import IssueForm, CommentForm
from issues.models import Issue, Comment, UserIssue
from projects.models import Project
from notifications.models import Change
from django.core.paginator import Paginator
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

    # Determine the sorting field and annotation
    if sort_by == 'title':
        issues = issues.annotate(lower_title=Lower('title')).order_by(f"{'' if order == 'asc' else '-'}lower_title")
    else:
        issues = issues.order_by(f"{'' if order == 'asc' else '-'}{sort_by}")

    # Pagination
    paginator = Paginator(issues, 12)  # 12 issues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    def toggle_order(current_order):
        return 'asc' if current_order == 'desc' else 'desc'

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
        'active_page': 'issues',
        'show_toast': show_toast,
        'page_obj': page_obj,
        'project': project,
        'sort_by': sort_by,
        'order': order,
        'toggle_order': toggle_order(order),
        'new_notifications': new_notifications,
    }

    return render(request, 'issues.html', context)

@login_required
def issue_detail(request, id):
    issue = get_object_or_404(Issue, id=id)
    comments = Comment.objects.filter(issue=issue).order_by('-commented_at')
    form = CommentForm()

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
        'issue': issue, 
        'comments': comments,
        'form': form, 
        'new_notifications': new_notifications,
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
        'issue': issue,
        'new_notifications': new_notifications,
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
