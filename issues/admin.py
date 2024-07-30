from django.contrib import admin
from django.utils.html import format_html
from issues.models import Issue, UserIssue, Comment


class IssueAdmin(admin.ModelAdmin):
    """ Admin interface options and customizations for the Issue model """
    list_display = (
        'id', 'title', 'severity', 'type', 'status', 'reporter', 'project',
        'developer', 'quality_assurance', 'product_manager'
    )
    fields = (
        'id', 'title', 'description', 'severity', 'type', 'status', 'reporter',
        'project', 'developer', 'quality_assurance', 'product_manager'
    )
    readonly_fields = ('id',)
    search_fields = ('title', 'reporter__username', 'project__title')
    list_filter = ('severity', 'type', 'status', 'project')
    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        """
        Automatically set the reporter to the current user if not specified,
        then call the parent class's save_model method to save the instance.
        """
        if not obj.reporter:
            obj.reporter = request.user
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    """ Admin interface options and customizations for the Comment model """
    list_display = (
        'id', 'comment_text', 'user', 'get_issue_id',
        'get_issue_title', 'commented_at'
    )
    fields = (
        'id', 'comment_text', 'user', 'issue'
    )
    readonly_fields = ('id', 'commented_at')
    search_fields = ('comment_text', 'user__username', 'issue__title')
    list_filter = ('user', 'commented_at')
    ordering = ('issue',)

    def get_issue_id(self, obj):
        """ Provide a clickable link to the related issue's change form """
        return format_html(
            '<a href="/admin/issues/issue/{}/change/">{}</a>',
            obj.issue.id, obj.issue.id
        )
    get_issue_id.short_description = 'Issue ID'

    def get_issue_title(self, obj):
        """ Return the title of the related issue """
        return obj.issue.title
    get_issue_title.short_description = 'Issue Title'

    def save_model(self, request, obj, form, change):
        """
        Automatically set the user to the current user if not specified,
        then call the parent class's save_model method to save the instance.
        """
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class UserIssueAdmin(admin.ModelAdmin):
    """ Admin interface options and customizations for the UserIssue model """
    list_display = (
        'user', 'get_issue_id', 'get_issue_title',
        'role', 'created_at'
    )
    fields = (
        'user', 'issue', 'role', 'created_at'
    )
    readonly_fields = ('created_at',)
    search_fields = ('user__username', 'issue__title', 'role')
    list_filter = ('user', 'role')
    ordering = ('issue',)

    def get_issue_id(self, obj):
        """ Provide a clickable link to the related issue's change form """
        return format_html(
            '<a href="/admin/issues/issue/{}/change/">{}</a>',
            obj.issue.id, obj.issue.id
        )
    get_issue_id.short_description = 'Issue ID'

    def get_issue_title(self, obj):
        """ Return the title of the related issue """
        return obj.issue.title
    get_issue_title.short_description = 'Issue Title'

    def save_model(self, request, obj, form, change):
        """ Call the parent class's save_model method to save the instance """
        super().save_model(request, obj, form, change)


# Register the models with the admin site
admin.site.register(Issue, IssueAdmin)
admin.site.register(UserIssue, UserIssueAdmin)
admin.site.register(Comment, CommentAdmin)
