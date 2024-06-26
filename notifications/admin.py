from django.contrib import admin
from .models import Change

class ChangeAdmin(admin.ModelAdmin):
    list_display = ('issue', 'user', 'changed_at', 'field_changed', 'old_value', 'new_value')
    readonly_fields = ('changed_at',)
    fields = ('issue', 'user', 'field_changed', 'old_value', 'new_value')
    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Change, ChangeAdmin)
