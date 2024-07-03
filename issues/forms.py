from django import forms
from issues.models import Issue, Comment

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'severity', 'project', 'type', 'status', 'developer', 'quality_assurance', 'product_manager']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']