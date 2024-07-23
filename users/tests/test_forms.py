from django.test import TestCase
from users.forms import CustomUserCreationForm, UserProfileForm
from users.models import User
from django.urls import reverse 

class CustomUserCreationFormTest(TestCase):
    """ Test case for the User Creation Form """
    def setUp(self):
        """ Set up the test data for Custom User Creation Form tests """
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
        """
        Test the User Creation Form with valid data.
        The form should be valid.
        """
        form = CustomUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_no_data(self):
        """
        Test the User Creation Form with no data.
        The form should be invalid and contain errors.
        """
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)  

    def test_custom_user_creation_form_missing_required_fields(self):
        """
        Test the User Creation Form with some required fields missing.
        The form should be invalid and contain errors for missing fields.
        """
        data = self.valid_data.copy()
        data['first_name'] = ''
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_custom_user_creation_form_password_mismatch(self):
        """
        Test the User Creation Form with mismatched passwords.
        The form should be invalid and contain errors for the password mismatch.
        """
        data = self.valid_data.copy()
        data['password2'] = 'differentpassword123'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_custom_user_creation_form_invalid_email(self):
        """
        Test the User Creation Form with an invalid email address.
        The form should be invalid and contain errors for the invalid email.
        """
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_creation_on_signup(self):
        """
        Test user creation via signup view.
        The response should redirect, and the user should be created.
        """
        response = self.client.post(reverse('signup'), data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

class UserProfileFormTest(TestCase):
    """ Test case for the User Profile Form """
    def setUp(self):
        """ Set up the test data for the User Profile Form tests """
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
        """
        Test the User Profile Form with valid data.
        The form should be valid.
        """
        form = UserProfileForm(data=self.valid_data, instance=self.user)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_no_data(self):
        """
        Test the User Profile Form with no data.
        The form should be invalid and contain errors.
        """
        form = UserProfileForm(data={}, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_user_profile_form_missing_required_fields(self):
        """
        Test the User Profile Form with some required fields missing.
        The form should be invalid and contain errors for missing fields.
        """
        data = self.valid_data.copy()
        data['first_name'] = ''
        form = UserProfileForm(data=data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_user_profile_form_invalid_email(self):
        """
        Test the User Profile Form with an invalid email address.
        The form should be invalid and contain errors for the invalid email.
        """
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        form = UserProfileForm(data=data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_profile_update(self):
        """
        Test updating the user profile form with valid data.
        The form should be valid, and the user instance should be updated.
        """
        form = UserProfileForm(data=self.valid_data, instance=self.user)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.email, 'updateduser@example.com')