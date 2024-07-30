from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    """ Form for creating and updating Projects """
    class Meta:
        """ Specifies the model to be used with this form and the fields
        that should be included in the form."""
        model = Project
        fields = ['title']
