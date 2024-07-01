from django.test import TestCase
from users.forms import CustomUserCreationForm
from users.models import User

# Create your tests here.

class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'role': 'developer',  
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_custom_user_creation_form_valid_data(self):
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_no_data(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)  

    def test_custom_user_creation_form_missing_required_fields(self):
        data = self.valid_data.copy()
        data['first_name'] = ''
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_custom_user_creation_form_password_mismatch(self):
        data = self.valid_data.copy()
        data['password2'] = 'differentpassword123'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_custom_user_creation_form_invalid_email(self):
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)