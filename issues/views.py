from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from issues.forms import IssueForm

# Create your views here.

def list_issues(request):
    show_toast = request.session.pop('registration_success', False)
    context = {
        'active_page': 'issues',
        'show_toast': show_toast
    }
    return render(request, 'issues.html', context)

# @login_required - uncomment this at the end if I want to restrict to logged in users only. 
def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reporter = request.user
            issue.save()
            return redirect('issue_list')  # Redirect to a list view of issues or any other appropriate view
    else:
        form = IssueForm()
    
    return render(request, 'create_issue.html', {'form': form})

def edit_issue(request):
    return render(request, 'editissue.html', {'active_page': 'issues'})