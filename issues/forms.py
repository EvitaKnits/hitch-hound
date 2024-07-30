from django import forms
from issues.models import Issue, Comment


class IssueForm(forms.ModelForm):
    """ A form for creating and updating Issue instances """
    class Meta:
        """ Specifies the model to be used with this form and the fields
        that should be included in the form."""
        model = Issue
        fields = [
            'title', 'description', 'severity', 'project', 'type',
            'status', 'developer', 'quality_assurance', 'product_manager'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            # Issue is new if instance doesn't exist so status not available
            self.fields.pop('status')

    def save(self, commit=True, user=None):
        """
        Custom save method to set the 'updated_by' field if a user is provided
        """
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
        """ Specifies the model to be used with this form and the fields
        that should be included in the form."""
        model = Comment
        fields = ['comment_text']
