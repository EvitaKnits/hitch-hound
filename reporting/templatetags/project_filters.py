from django import template
from projects.models import Project

register = template.Library()

@register.filter
def get_project_title(projects, project_id):
    try:
        project = projects.get(id=project_id)
        return project.title
    except Project.DoesNotExist:
        return ''