from django.contrib import admin
from .models import Issue, UserIssue, Comment

class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'type', 'status', 'reporter', 'project_title', 'developer', 'quality_assurance', 'product_manager')
    fields = ('title', 'description', 'severity', 'type', 'status', 'reporter', 'project_title', 'developer', 'quality_assurance', 'product_manager')
    search_fields = ('title', 'reporter__username', 'project_title__name')
    list_filter = ('severity', 'type', 'status', 'project_title')

    def save_model(self, request, obj, form, change):
        if not obj.reporter:
            obj.reporter = request.user
        super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'user_id', 'issue_id', 'commented_at')
    fields = ('comment_text', 'user_id', 'issue_id')
    readonly_fields = ('comment_id', 'commented_at')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Issue, IssueAdmin)
admin.site.register(UserIssue)
admin.site.register(Comment, CommentAdmin)
