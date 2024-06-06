from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def list_issues(request):
    return render(request, 'issues.html', {'active_page': 'issues'})

def create_issue(request):
    return render(request, 'newissue.html', {'active_page': 'issues'})

def edit_issue(request):
    return render(request, 'editissue.html', {'active_page': 'issues'})