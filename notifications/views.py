from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from notifications.models import Change
from issues.models import Issue 

# Create your views here.

def list_notifications(request):
    return render(request, 'notifications.html')

def change_history(request, issue_id=None):
    if issue_id:
        changes = Change.objects.filter(issue_id=issue_id).order_by('-changed_at')
    else:
        changes = Change.objects.all().order_by('-changed_at')
    return render(request, 'change_history.html', {'changes': changes})