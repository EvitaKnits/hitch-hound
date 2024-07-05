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
    
    def save(self, *args, **kwargs):
        if 'user' in kwargs:
            self.updated_by = kwargs.pop('user')
        super().save(*args, **kwargs)

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