from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from issues.forms import IssueForm
from issues.models import Issue

# Create your views here.

# @login_required - uncomment this at the end if I want to restrict to logged in users only. 
def list_issues(request):
    show_toast = request.session.pop('registration_success', False)
    sort = request.GET.get('sort', 'title')
    project_id = request.GET.get('project_id')

    if project_id:
        project = get_object_or_404(Project, id=project_id)
        issues = Issue.objects.filter(project_title=project).order_by(sort)
    else:
        issues = Issue.objects.all().order_by(sort)

    context = {
        'active_page': 'issues',
        'show_toast': show_toast,
        'issues': issues,
        'project': project if project_id else None,
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
