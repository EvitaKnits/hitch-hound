from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'severity', 'project_title', 'type', 'status', 'developer', 'quality_assurance', 'product_manager']