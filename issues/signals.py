from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Issue, UserIssue

@receiver(post_save, sender=Issue)
def manage_user_issue(sender, instance, created, **kwargs):
    # Clear existing UserIssue entries for this issue
    UserIssue.objects.filter(issue=instance).delete()

    # Create UserIssue entries for each assigned role
    if instance.developer:
        UserIssue.objects.create(user=instance.developer, issue=instance, role='developer')
    if instance.quality_assurance:
        UserIssue.objects.create(user=instance.quality_assurance, issue=instance, role='quality_assurance')
    if instance.product_manager:
        UserIssue.objects.create(user=instance.product_manager, issue=instance, role='product_manager')