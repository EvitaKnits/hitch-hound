from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'role', 'password1', 'password2')