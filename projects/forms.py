from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    """ Form for creating and updating Projects """
    class Meta: 
        model = Project
        fields = ['title']