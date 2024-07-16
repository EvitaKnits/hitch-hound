from django.test import TestCase
from users.forms import CustomUserCreationForm, UserProfileForm
from users.models import User
from django.urls import reverse 

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

    def test_user_creation_on_signup(self):
        response = self.client.post(reverse('signup'), data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            role='developer'
        )
        self.valid_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updateduser@example.com',
        }

    def test_user_profile_form_valid_data(self):
        form = UserProfileForm(data=self.valid_data, instance=self.user)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_no_data(self):
        form = UserProfileForm(data={}, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_user_profile_form_missing_required_fields(self):
        data = self.valid_data.copy()
        data['first_name'] = ''
        form = UserProfileForm(data=data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_user_profile_form_invalid_email(self):
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        form = UserProfileForm(data=data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_profile_update(self):
        form = UserProfileForm(data=self.valid_data, instance=self.user)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.email, 'updateduser@example.com')