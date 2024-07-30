from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from issues.models import Issue, UserIssue
from notifications.models import Change

User = get_user_model()


@receiver(post_save, sender=Issue)
def manage_user_issue(sender, instance, created, **kwargs):
    """
    Signal handler to manage UserIssue entries after an Issue is saved.
    This function ensures that the UserIssue entries are updated to reflect
    the current assignments for the developer, quality assurance, and product
    manager roles.
    """
    # Clear existing UserIssue entries for this issue
    UserIssue.objects.filter(issue=instance).delete()

    # Create UserIssue entries for each assigned role
    if instance.developer:
        UserIssue.objects.create(
            user=instance.developer, issue=instance, role='developer'
        )
    if instance.quality_assurance:
        UserIssue.objects.create(
            user=instance.quality_assurance,
            issue=instance,
            role='quality_assurance'
        )
    if instance.product_manager:
        UserIssue.objects.create(
            user=instance.product_manager,
            issue=instance,
            role='product_manager'
        )


@receiver(pre_save, sender=Issue)
def create_change_record(sender, instance, **kwargs):
    """
    Signal handler to create a Change record before an Issue is saved.
    This function tracks changes to specified fields and logs them in the
    Change model.
    """
    # Skip creation if the instance is new and does not have a primary key yet
    if not instance.pk:
        return

    # Get the existing issue from the database
    old_issue = Issue.objects.get(pk=instance.pk)
    fields_to_track = [field[0] for field in Change.FIELD_CHOICES]

    # Compare old and new values for each tracked field
    for field in fields_to_track:
        old_value = getattr(old_issue, field)
        new_value = getattr(instance, field)

        # Create a Change record if the value has changed
        if old_value != new_value:
            Change.objects.create(
                issue=instance,
                user=instance.updated_by,
                field_changed=field,
                old_value=str(old_value),
                new_value=str(new_value),
            )
