from django.db import models
from projects.models import Project
from users.models import User 

class Issue(models.Model):
    """
    This model represents an issue with various attributes, which is assigned to a project.
    """
    SEVERITY_CHOICES = (   
        (1, '1 - Critical'),
        (2, '2 - High'),
        (3, '3 - Medium'),
        (4, '4 - Low'),
    )
    TYPE_CHOICES = (
        ('bug', 'Bug'),
        ('missed_requirement', 'Missed Requirement'),
        ('other', 'Other Issue'),
    )
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('testing', 'Testing'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    )

    title = models.CharField(max_length=255, null=False)
    description = models.TextField()
    severity = models.IntegerField(choices=SEVERITY_CHOICES, default=4)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='bug')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    developer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'developer'}, related_name='developer_issues')
    quality_assurance = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'quality_assurance'}, related_name='qa_issues')
    product_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'product_manager'}, related_name='pm_issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_issues')

    def get_allowed_statuses_for_role(self, role):
        """ Return a list of allowed statuses for a given role to power permissions """
        if role == 'developer':
            return ['open', 'in_progress']
        elif role == 'quality_assurance':
            return ['open', 'testing']
        elif role == 'product_manager':
            return ['open', 'approved', 'closed', 'cancelled']
        elif role == 'superuser':
            return ['open', 'in_progress', 'testing', 'approved', 'closed', 'cancelled']
        return ['open']

    def can_user_update_status(self, user, new_status):
        """ Check if a user has permission to update the issue status """
        if user is None:
            return False
        if user.is_superuser:
            return True
        role = user.role
        allowed_statuses = self.get_allowed_statuses_for_role(role)
        print(f'User Role: {role}, Attempted Status: {new_status}, Allowed Statuses: {allowed_statuses}')
        return new_status in allowed_statuses

    def save(self, *args, **kwargs):
        """
        Override the save method to include custom logic for updating the issue.
        
        If a user is provided via kwargs, set the `updated_by` field to that user.
        Before saving, if the status of the issue is being changed, verify that the 
        user has the necessary permissions to change to the new status. If the user 
        lacks the required permissions, the save operation is aborted.
        """
        user = kwargs.pop('user', None)
        if user:
            self.updated_by = user

        # Only enforce permissions if the status is being changed
        if self.pk:
            old_issue = Issue.objects.get(pk=self.pk)
            if old_issue.status != self.status:
                if not self.can_user_update_status(user, self.status):
                    return False

        super().save(*args, **kwargs)
        return True

class UserIssue(models.Model):
    """
    Intermediate model to link users to specific roles on specific issues.
    """
    ROLE_CHOICES = (
        ('developer', 'Developer'),
        ('quality_assurance', 'Quality Assurance'),
        ('product_manager', 'Product Manager'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    # Ensure unique assignments of user to issue with a specific role
    class Meta:
        unique_together = ('user', 'issue', 'role')

class Comment(models.Model):
    """ This model represents a comment made on an issue """
    comment_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ Return a truncated string representation of the comment """
        return self.comment_text[:20]