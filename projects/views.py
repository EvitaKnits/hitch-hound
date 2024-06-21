from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from projects.models import Project
from issues.models import Issue
from django.core.paginator import Paginator

# Create your views here.

def list_projects(request):
    projects = Project.objects.all()
    for project in projects:
        project.latest_issues = Issue.objects.filter(project_title=project).order_by('-created_at')[:3]

    return render(request, 'projects.html', {'projects': projects})

def view_all_issues(request, project_title):
    project = get_object_or_404(Project, title=project_title)
    issues = Issue.objects.filter(project_title=project)

    # Sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order = request.GET.get('order', 'desc')
    if order == 'asc':
        issues = issues.order_by(sort_by)
    else:
        issues = issues.order_by(f'-{sort_by}')

    # Pagination
    paginator = Paginator(issues, 10)  # Show 10 issues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Toggle order for sorting links
    toggle_order = 'asc' if order == 'desc' else 'desc'

    context = {
        'project': project,
        'page_obj': page_obj,
        'sort_by': sort_by,
        'order': order,
        'toggle_order': toggle_order,
    }
    return render(request, 'all_issues.html', context)

def create_project(request):
    return render(request, 'create_project.html')

def edit_project(request):
    return render(request, 'edit_project.html')