from django.contrib import admin
from .models import Issue, UserIssue, Comment

# Register your models here.

admin.site.register(Issue)
admin.site.register(UserIssue)
admin.site.register(Comment)
