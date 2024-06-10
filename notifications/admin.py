from django.contrib import admin
from .models import Change

class ChangeAdmin(admin.ModelAdmin):
    readonly_fields = [
        'change_id',
        'issue',
        'user',
        'changed_at',
        'field_changed',
        'old_value',
        'new_value'
    ]

# Register your models here.

admin.site.register(Change, ChangeAdmin)