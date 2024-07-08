from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
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
