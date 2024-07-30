from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from notifications.models import Change
from issues.models import Issue, UserIssue
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from hitchhound.utils import paginate, get_new_notifications
from django.utils import timezone


@login_required
def list_notifications(request):
    """
    View to list notifications for the logged-in user.
    Displays changes related to issues the user is assigned to or has reported,
    excluding changes made by the user themselves.
    """
    current_user = request.user

    # Check if there are new notifications
    new_notifications = get_new_notifications(current_user)

    # Fetch issues the user is assigned to
    user_issues = UserIssue.objects.filter(
        user=current_user
    ).values_list(
        'issue', flat=True
    )

    # Fetch changes for user's issues, excluding changes made by the user
    changes = Change.objects.filter(
        Q(issue_id__in=user_issues) | Q(issue__reporter=current_user)
    ).exclude(user=current_user)

    # Combine all notifications into a single list and sort by date
    notifications = changes.order_by('-changed_at')

    # Use the paginate utility function
    page_obj = paginate(request, notifications)

    # Update the last visited timestamp after checking for new notifications
    current_user.last_visited_notifications = timezone.now()
    current_user.save()

    context = {
        'page_obj': page_obj,
        'new_notifications': new_notifications,
        'show_navbar': True,
    }

    return render(request, 'notifications.html', context)


@login_required
def change_history(request, issue_id):
    """ View to display the change history of a specific issue """
    # Ensure the issue exists
    issue = get_object_or_404(Issue, pk=issue_id)

    # Fetch all changes for the specific issue, ordered by the change date
    changes = Change.objects.filter(issue=issue).order_by('-changed_at')

    # Calculate new notifications for the current user
    new_notifications = get_new_notifications(request.user)

    # Use the paginate utility function to handle pagination
    page_obj = paginate(request, changes)

    context = {
        'page_obj': page_obj,
        'changes': changes,
        'new_notifications': new_notifications,
        'issue': issue,
        'active_page': 'issues',
        'show_navbar': True,
    }

    return render(request, 'change_history.html', context)
