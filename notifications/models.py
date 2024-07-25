from django.db import models
from issues.models import Issue
from users.models import User

class Change(models.Model):
    """
    Model to represent changes made to issues.
    Each instance records a change to a specific field of an issue by a user.
    """
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
        """
        Return a string representation of the change.
        """
        return f'{self.field_changed} changed from {self.old_value} to {self.new_value} by {self.user}'

    def get_field_changed_display(self):
        return dict(self.FIELD_CHOICES).get(self.field_changed, self.field_changed)

    def get_display_value(self, value, field_name):
        # Fetch the Issue model field choices dynamically
        issue_field_choices = {
            'status': Issue.STATUS_CHOICES,
            'severity': Issue.SEVERITY_CHOICES,
            'type': Issue.TYPE_CHOICES,
        }

        # Check if the field has defined choices
        if field_name in issue_field_choices:
            choices_dict = dict(issue_field_choices[field_name])
            # Convert value to int if the field is severity and value is a string
            if field_name == 'severity' and isinstance(value, str):
                value = int(value)
            return choices_dict.get(value, value)
        return value

    def get_old_value_display(self):
        return self.get_display_value(self.old_value, self.field_changed)

    def get_new_value_display(self):
        return self.get_display_value(self.new_value, self.field_changed)