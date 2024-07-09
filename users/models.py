from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager, Group
from django.utils import timezone

# Create your models here.

class UserManager(DefaultUserManager):
    def developers(self):
        return self.filter(role='developer')

    def quality_assurance(self):
        return self.filter(role='quality_assurance')

    def product_managers(self):
        return self.filter(role='product_manager')

class User(AbstractUser):
    ROLE_CHOICES = (
        ('developer', 'Developer'),
        ('quality_assurance', 'Quality Assurance'),
        ('product_manager', 'Product Manager'),
    )
    role = models.CharField(max_length=20, null=False, choices=ROLE_CHOICES, default='developer')
    last_visited_notifications = models.DateTimeField(null=True, blank=True)

    objects = UserManager() 

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
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
