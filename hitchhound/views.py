from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from notifications.models import Change
from issues.models import UserIssue
from hitchhound.utils import get_new_notifications

def custom_404(request, exception):
    """
    Custom 404 error handler.

    Parameters:
    - request: The HttpRequest object.
    - exception: The exception object raised.

    Returns:
    - HttpResponse: The response object with a rendered 404 page.
    """

    # Calls the utility function to check for new notifications for the current user
    new_notifications = get_new_notifications(request.user)

    context = {
        'new_notifications': new_notifications,
        'show_navbar': True,
    }

    return render(request, '404.html', context, status=404)
