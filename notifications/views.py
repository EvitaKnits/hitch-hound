from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from notifications.models import Change
from issues.models import Issue, UserIssue
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone



# Create your views here.

@login_required
def list_notifications(request):
    current_user = request.user

    # Update the last visited timestamp
    current_user.last_visited_notifications = timezone.now()
    current_user.save()

    # Fetch issues the user is assigned to
    user_issues = UserIssue.objects.filter(user=current_user).values_list('issue', flat=True)

    # Fetch changes for issues the user is assigned to or where the user is the reporter, excluding changes made by the user
    changes = Change.objects.filter(
        Q(issue_id__in=user_issues) | Q(issue__reporter=current_user)
    ).exclude(user=current_user)

    # Determine if there are new notifications
    last_visited = current_user.last_visited_notifications or timezone.now()
    new_notifications = changes.filter(changed_at__gt=last_visited).exists()

    # Combine all notifications into a single list and sort by date
    notifications = list(changes)
    notifications.sort(key=lambda x: x.changed_at if isinstance(x, Change) else x.created_at, reverse=True)

    paginator = Paginator(notifications, 12)  # 12 notifications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'new_notifications': new_notifications,
    }

    return render(request, 'notifications.html', context)

def change_history(request, issue_id=None):
    if issue_id:
        changes = Change.objects.filter(issue_id=issue_id).order_by('-changed_at')
    else:
        changes = Change.objects.all().order_by('-changed_at')

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
        'changes': changes,
        'new_notifications': new_notifications,
    }

    return render(request, 'change_history.html', context)