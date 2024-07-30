from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from users.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating new users. Extends the default UserCreationForm
    and includes additional fields for first name, last name, email, and role.
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'autofocus': 'autofocus'}
        )
    )

    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        """
        Meta class to specify the model and fields to include in the form
        """
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove autofocus from username field
        self.fields['username'].widget.attrs.pop('autofocus', None)


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profiles. Includes fields for first name, last name,
    and email.
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'autofocus': 'autofocus'}
        )
    )
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        """
        Meta class to specify the model and fields to include in the form
        """
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set up the Crispy Forms helper for better form
        layout.
        """
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
