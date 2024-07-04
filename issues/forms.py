from django import forms
from issues.models import Issue, Comment

from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'severity', 'project', 'type', 'status', 'developer', 'quality_assurance', 'product_manager']

    def save(self, commit=True, user=None):
        issue = super().save(commit=False)
        if user:
            issue.updated_by = user
        if commit:
            issue.save()
        return issue

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']