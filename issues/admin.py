from django.contrib import admin
from django.utils.html import format_html
from issues.models import Issue, UserIssue, Comment

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'severity', 'type', 'status', 'reporter', 'project', 'developer', 'quality_assurance', 'product_manager')
    fields = ('id', 'title', 'description', 'severity', 'type', 'status', 'reporter', 'project', 'developer', 'quality_assurance', 'product_manager')
    readonly_fields = ('id',)
    search_fields = ('title', 'reporter__username', 'project__title')
    list_filter = ('severity', 'type', 'status', 'project')
    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if not obj.reporter:
            obj.reporter = request.user
        super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_text', 'user', 'get_issue_id', 'get_issue_title', 'commented_at')
    fields = ('id', 'comment_text', 'user', 'issue')
    readonly_fields = ('id', 'commented_at',)
    search_fields = ('comment_text', 'user__username', 'issue__title')
    list_filter = ('user', 'commented_at')
    ordering = ('issue',)

    def get_issue_id(self, obj):
        return format_html('<a href="/admin/issues/issue/{}/change/">{}</a>', obj.issue.id, obj.issue.id)
    get_issue_id.short_description = 'Issue ID'

    def get_issue_title(self, obj):
        return obj.issue.title
    get_issue_title.short_description = 'Issue Title'

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

class UserIssueAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_issue_id', 'get_issue_title', 'role', 'created_at')
    fields = ('user', 'issue', 'role', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('user__username', 'issue__title', 'role')
    list_filter = ('user', 'role')
    ordering = ('issue',)

    def get_issue_id(self, obj):
        return format_html('<a href="/admin/issues/issue/{}/change/">{}</a>', obj.issue.id, obj.issue.id)
    get_issue_id.short_description = 'Issue ID'

    def get_issue_title(self, obj):
        return obj.issue.title
    get_issue_title.short_description = 'Issue Title'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Issue, IssueAdmin)
admin.site.register(UserIssue, UserIssueAdmin)
admin.site.register(Comment, CommentAdmin)