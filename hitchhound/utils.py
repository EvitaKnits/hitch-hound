from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from notifications.models import Change
from issues.models import UserIssue

def paginate(request, queryset, per_page=12):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def get_new_notifications(user):
    """
    Utility function to calculate if there are new notifications for a user.
    
    Parameters:
    - user: The user for whom to check notifications.

    Returns:
    - boolean: True if there are new notifications, False otherwise.
    """
    last_visited = user.last_visited_notifications or timezone.now()

    # Fetch issues the user is assigned to
    user_issues = UserIssue.objects.filter(user=user).values_list('issue', flat=True)

    # Fetch changes for issues the user is assigned to or where the user is the reporter, excluding changes made by the user
    changes = Change.objects.filter(
        Q(issue_id__in=user_issues) | Q(issue__reporter=user)
    ).exclude(user=user)

    # Determine if there are new notifications
    new_notifications = changes.filter(changed_at__gt=last_visited).exists()
    
    return new_notifications