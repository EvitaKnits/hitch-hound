from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from issues.forms import IssueForm
from issues.models import Issue
from projects.models import Project
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import F

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

    context = {
        'active_page': 'issues',
        'show_toast': show_toast,
        'page_obj': page_obj,
        'project': project,
        'sort_by': sort_by,
        'order': order,
        'toggle_order': toggle_order(order),
    }

    return render(request, 'issues.html', context)

def issue_detail(request, id):
    issue = get_object_or_404(Issue, id=id)
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

def edit_issue(request, id):
    issue = get_object_or_404(Issue, id=id)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('issue_detail', id=issue.id)
    else:
        form = IssueForm(instance=issue)
    return render(request, 'edit_issue.html', {'form': form, 'issue': issue})

@login_required
def delete_issue(request, id):
    issue = get_object_or_404(Issue, id=id)
    if request.method == 'POST':
        issue.delete()
        return redirect('issues')
    return redirect('issue_detail', id=id)
