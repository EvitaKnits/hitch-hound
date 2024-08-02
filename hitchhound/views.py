"""
This module provides a custom 404 error handler across the whole project.
"""

from django.shortcuts import render
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

    context = {
        'new_notifications': get_new_notifications(request.user),
        'show_navbar': True,
    }

    return render(request, '404.html', context, status=404)
