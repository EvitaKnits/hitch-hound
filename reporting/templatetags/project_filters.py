from django import template
from projects.models import Project

# Register the template library to create custom template tags and filters
register = template.Library()


@register.filter
def get_project_title(projects, project_id):
    """
    Custom template filter to get the title of a project by its ID.

    Args:
        projects (QuerySet): The QuerySet of Project objects.
        project_id (int): The ID of the project to retrieve the title for.

    Returns:
        str: The title of the project if found, otherwise an empty string.
    """
    try:
        project = projects.get(id=project_id)
        return project.title
    except Project.DoesNotExist:
        return ''
