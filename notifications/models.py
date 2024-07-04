from django.db import models
from issues.models import Issue
from users.models import User

# Create your models here.

class Change(models.Model):
    FIELD_CHOICES = (
        ('title', 'Title'),
        ('description', 'Description'),
        ('severity', 'Severity'),
        ('project', 'Project'),
        ('type', 'Type'),
        ('status', 'Status'),
        ('developer', 'Developer'),
        ('quality_assurance', 'Quality Assurance'),
        ('product_manager', 'Product Manager'),
    )

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    field_changed = models.CharField(max_length=50, choices=FIELD_CHOICES)
    old_value = models.TextField()
    new_value = models.TextField()

    def __str__(self):
        return f'{self.field_changed} changed from {self.old_value} to {self.new_value} by {self.user}'