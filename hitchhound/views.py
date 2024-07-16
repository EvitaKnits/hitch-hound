from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from notifications.models import Change
from issues.models import UserIssue
from hitchhound.utils import get_new_notifications

def custom_404(request, exception):

    # Calculate new notifications
    new_notifications = get_new_notifications(request.user)

    context = {
        'new_notifications': new_notifications,
    }

    return render(request, '404.html', context, status=404)
