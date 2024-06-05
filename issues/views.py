from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def list_issues(request):
    return render(request, 'issues.html')

def create_issue(request):
    return HttpResponse("This is the create a new issue page")

def edit_issue(request):
    return HttpResponse("This is the edit issue page")