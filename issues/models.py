from django.db import models
from projects.models import Project
from users.models import User 

# Create your models here.

class Issue(models.Model):
    SEVERITY_CHOICES = (   
        ('critical', '1 - Critical'),
        ('high', '2 - High'),
        ('medium', '3 - Medium'),
        ('low', '4 - Low'),
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
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='low')
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
        if user is None:
            return False
        if user.is_superuser:
            return True
        role = user.role
        allowed_statuses = self.get_allowed_statuses_for_role(role)
        print(f"User Role: {role}, Attempted Status: {new_status}, Allowed Statuses: {allowed_statuses}")
        return new_status in allowed_statuses

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            self.updated_by = user

        # Only enforce permissions if the status is being changed
        if self.pk:
            old_issue = Issue.objects.get(pk=self.pk)
            if old_issue.status != self.status:
                if not self.can_user_update_status(user, self.status):
                    return False  # Return False if permission is denied

        super().save(*args, **kwargs)
        return True  # Return True if save is successful

class UserIssue(models.Model):
    ROLE_CHOICES = (
        ('developer', 'Developer'),
        ('quality_assurance', 'Quality Assurance'),
        ('product_manager', 'Product Manager'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'issue', 'role')

class Comment(models.Model):

    comment_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text[:20]