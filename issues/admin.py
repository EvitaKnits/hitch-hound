from django.contrib import admin
from .models import Issue, UserIssue, Comment

class IssueAdmin(admin.ModelAdmin):
    readonly_fields = [
        'issue_id',
        'reporter'
    ]

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = [
    'comment_id',
    'user_id',
    'issue_id', 
    'commented_at',
    ]

# Register your models here.

admin.site.register(Issue, IssueAdmin)
admin.site.register(UserIssue)
admin.site.register(Comment, CommentAdmin)
