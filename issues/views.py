from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def list_issues(request):
    show_toast = request.session.pop('registration_success', False)
    context = {
        'active_page': 'issues',
        'show_toast': show_toast
    }
    return render(request, 'issues.html', context)

def create_issue(request):
    return render(request, 'newissue.html', {'active_page': 'issues'})

def edit_issue(request):
    return render(request, 'editissue.html', {'active_page': 'issues'})