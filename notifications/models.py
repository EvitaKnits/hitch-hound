from django.db import models
from issues.models import Issue
from users.models import User

# Create your models here.

class Change(models.Model):
    FIELD_CHOICES = (
        ('title', 'Title'),
        ('description', 'Description'),
        ('severity', 'Severity'),
        ('project_title', 'Project Title'),
        ('type', 'Type'),
        ('status', 'Status'),
        ('developer', 'Developer'),
        ('quality_assurance', 'Quality Assurance'),
        ('product_manager', 'Product Manager'),
    )

    change_id = models.AutoField(primary_key=True, editable=False)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    changed_at = models.DateTimeField(auto_now_add=True, editable=False)
    field_changed = models.CharField(max_length=50, choices=FIELD_CHOICES, editable=False)
    old_value = models.CharField(max_length=255, editable=False)
    new_value = models.CharField(max_length=255, editable=False)
