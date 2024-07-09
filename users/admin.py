from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'last_login', 'last_visited_notifications')
    fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'last_login', 'last_visited_notifications', 'groups')
    readonly_fields = ('id', 'last_login', 'last_visited_notifications')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role', 'last_login', 'groups')
    ordering = ('id',)
    filter_horizontal = ('groups',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(User, UserAdmin)
