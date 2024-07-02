from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,  widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'role', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True,  widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            'role',
        )
        self.helper.add_input(Submit('submit', 'Save Changes'))