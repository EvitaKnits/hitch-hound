from django import forms
from issues.models import Issue, Comment

class IssueForm(forms.ModelForm):
    """ A form for creating and updating Issue instances """
    class Meta:
        model = Issue
        fields = ['title', 'description', 'severity', 'project', 'type', 'status', 'developer', 'quality_assurance', 'product_manager']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            # If instance doesn't exist, its a new issue so status field shouldn't be available 
            self.fields.pop('status')

    def save(self, commit=True, user=None):
        """ Custom save method to set the 'updated_by' field if a user is provided """
        issue = super().save(commit=False)
        if user:
            issue.updated_by = user
        if commit:
            success = issue.save(user=user)
            return success
        return issue

class CommentForm(forms.ModelForm):
    """ A form for creating Comment instances """
    class Meta:
        model = Comment
        fields = ['comment_text']