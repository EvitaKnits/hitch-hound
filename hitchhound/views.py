from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from notifications.models import Change
from issues.models import UserIssue


def custom_404(request, exception):

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
        'new_notifications': new_notifications,
    }

    return render(request, '404.html', context, status=404)
