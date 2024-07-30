from django.contrib import admin
from django.utils.html import format_html
from .models import Change


class ChangeAdmin(admin.ModelAdmin):
    """ Custom admin interface for the Change model """
    list_display = (
        'id', 'get_issue_id', 'get_issue_title', 'user', 'field_changed',
        'old_value', 'new_value', 'changed_at'
    )
    readonly_fields = ('changed_at', 'id')
    fields = (
        'id', 'issue', 'user', 'field_changed', 'old_value', 'new_value'
    )
    search_fields = (
        'issue__title', 'user__username', 'field_changed', 'old_value',
        'new_value'
    )
    list_filter = ('field_changed', 'changed_at', 'user')
    ordering = ('id',)

    def get_issue_id(self, obj):
        """ Provide a clickable link to the related issue """
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
        """ Automatically set the user to the current user if not specified """
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


# Register the Change model with the custom admin interface
admin.site.register(Change, ChangeAdmin)
