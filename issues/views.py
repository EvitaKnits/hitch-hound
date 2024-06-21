from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from issues.forms import IssueForm
from issues.models import Issue
from projects.models import Project
from django.core.paginator import Paginator

# Create your views here.

# @login_required - uncomment this at the end if I want to restrict to logged in users only. 
def list_issues(request):
    show_toast = request.session.pop('registration_success', False)
    sort_by = request.GET.get('sort_by', 'title')
    order = request.GET.get('order', 'asc')
    project_id = request.GET.get('project_id')
    
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        issues = Issue.objects.filter(project_title=project)
    else:
        issues = Issue.objects.all()

    if order == 'desc':
        sort_by = '-' + sort_by

    issues = issues.order_by(sort_by)

    # Pagination
    paginator = Paginator(issues, 12)  # 12 issues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    def toggle_order(current_order):
        return 'asc' if current_order == 'desc' else 'desc'

    context = {
        'active_page': 'issues',
        'show_toast': show_toast,
        'page_obj': page_obj,  # Use page_obj instead of issues
        'project': project if project_id else None,
        'sort_by': sort_by.strip('-'),
        'order': order,
        'toggle_order': toggle_order(order)
    }

    return render(request, 'issues.html', context)

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'issue_detail.html', {'issue': issue})

# @login_required - uncomment this at the end if I want to restrict to logged in users only. 
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
    
    return render(request, 'create_issue.html', {'form': form})

def edit_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('issue_detail', issue_id=issue.issue_id)
    else:
        form = IssueForm(instance=issue)
    return render(request, 'edit_issue.html', {'form': form, 'issue': issue})
