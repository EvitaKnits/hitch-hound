from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from notifications.models import Change
from issues.models import UserIssue

def paginate(request, queryset, per_page=12):
    """
    Paginate a given queryset for a Django view.

    Parameters:
    - request: The HttpRequest object.
    - queryset: The queryset to paginate.
    - per_page: Number of items per page (default is 12).

    Returns:
    - page_obj: The Page object containing the items for the current page.
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def get_new_notifications(user):
    """
    Calculate whether there are new notifications for a user.
    
    Parameters:
    - user: The user for whom to check notifications.

    Returns:
    - boolean: True if there are new notifications, False otherwise.

    The function checks for new changes related to issues the user is assigned to or has reported,
    excluding changes made by the user, since the user's last visit to the notifications page.
    """
    # Get last time the user visited notifications page, or use current time if never visited
    last_visited = user.last_visited_notifications or timezone.now()

    # Fetch issues the user is assigned to
    user_issues = UserIssue.objects.filter(user=user).values_list('issue', flat=True)

    # Fetch changes for issues the user reported/is assigned to, excluding changes made by the user
    changes = Change.objects.filter(
        Q(issue_id__in=user_issues) | Q(issue__reporter=user)
    ).exclude(user=user)

    # Check if any changes made by another user since the user's last visit
    new_notifications = changes.filter(changed_at__gt=last_visited).exists()
    
    return new_notifications