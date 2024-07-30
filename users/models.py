from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.utils import timezone


class UserManager(DefaultUserManager):
    """
    Custom manager for User model with methods to filter users by role.
    """
    def developers(self):
        return self.filter(role='developer')

    def quality_assurance(self):
        return self.filter(role='quality_assurance')

    def product_managers(self):
        return self.filter(role='product_manager')


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds a role field and last_visited_notifications field.
    """
    ROLE_CHOICES = (
        ('developer', 'Developer'),
        ('quality_assurance', 'Quality Assurance'),
        ('product_manager', 'Product Manager'),
    )
    role = models.CharField(
        max_length=20, null=False, choices=ROLE_CHOICES, default='developer'
    )
    last_visited_notifications = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(unique=True)

    objects = UserManager()

    def __str__(self):
        """
        Return the string representation of the user, which is the username.
        """
        return self.username

    def save(self, *args, **kwargs):
        """
        Override the save method to assign the user to a group based on their
        role.
        """
        super().save(*args, **kwargs)
        role_group_map = {
            'developer': 'Developers',
            'quality_assurance': 'Quality Assurance',
            'product_manager': 'Product Managers'
        }
        group_name = role_group_map.get(self.role)
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            self.groups.set([group])
