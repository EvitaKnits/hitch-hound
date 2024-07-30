from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from users.forms import CustomUserCreationForm, UserProfileForm
from issues.models import Issue, Project

User = get_user_model()


class UserViewsTest(TestCase):
    """ Test case for user-related views """

    def setUp(self):
        """
        Set up the test data for user-related view tests.
        Create a user, project, and issues for testing.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.project = Project.objects.create(title='Test Project')
        self.issue1 = Issue.objects.create(
            title='Issue 1', reporter=self.user, project=self.project
        )
        self.issue2 = Issue.objects.create(
            title='Issue 2', reporter=self.user, project=self.project
        )

    def test_user_login_get(self):
        """
        Test the GET request for the login view.
        Ensure the login page loads correctly with the right template.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_login_post_success(self):
        """
        Test the POST request for the login view with valid credentials.
        Ensure the user is redirected to the home page after a successful login
        """
        response = self.client.post(
            reverse('login'), {'username': 'testuser', 'password': 'password'}
        )
        self.assertRedirects(response, reverse('home'))

    def test_user_login_post_failure(self):
        """
        Test the POST request for the login view with invalid credentials.
        Ensure the login page reloads with an error message.
        """
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'wrongpassword'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn(
            'Invalid username or password.', response.content.decode()
        )

    def test_user_signup_get(self):
        """
        Test the GET request for the signup view.
        Ensure the signup page loads correctly with the right template and form
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_user_signup_post_success(self):
        """
        Test the POST request for the signup view with valid data.
        Ensure the user is created and redirected to the home page after a
        successful signup.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123',
            'first_name': 'First',
            'last_name': 'Last',
            'role': 'developer'
        })
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_signup_post_failure(self):
        """
        Test the POST request for the signup view with invalid data.
        Ensure the signup page reloads with the form and error messages.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'wrongpassword',
            'first_name': 'First',
            'last_name': 'Last',
            'role': 'quality_assurance'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_password_reset_get(self):
        """
        Test the GET request for the password reset view.
        Ensure the password reset page loads correctly with the right template
        and form.
        """
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/password_reset_form.html'
        )
        self.assertIsInstance(response.context['form'], PasswordResetForm)

    def test_password_reset_post_success(self):
        """
        Test the POST request for the password reset view with a valid email.
        Ensure the user is redirected and a password reset email is sent.
        """
        response = self.client.post(
            reverse('password_reset'), {'email': 'testuser@example.com'}
        )
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password reset', mail.outbox[0].subject)

    def test_password_reset_post_failure(self):
        """
        Test the POST request for the password reset view with an invalid
        email. Ensure the user is redirected and no email is sent.
        """
        response = self.client.post(
            reverse('password_reset'), {'email': 'nonexistent@example.com'}
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_done(self):
        """
        Test the GET request for the password reset done view.
        Ensure the page loads correctly with the right template.
        """
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/password_reset_done.html'
        )

    def test_password_reset_complete(self):
        """
        Test the GET request for the password reset complete view.
        Ensure the page loads correctly with the right template.
        """
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/password_reset_complete.html'
        )

    def test_user_profile(self):
        """
        Test the GET request for the user profile view.
        Ensure the profile page loads correctly with the right template and
        form.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertIsInstance(response.context['form'], UserProfileForm)

    def test_change_password_get(self):
        """
        Test the GET request for the change password view.
        Ensure the change password page loads correctly with the right template
        and form.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        self.assertIsInstance(
            response.context['password_change_form'], PasswordChangeForm
        )

    def test_change_password_post_success(self):
        """
        Test the POST request for the change password view with valid data.
        Ensure the user is redirected to the profile page after a successful
        password change.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('change_password'), {
            'old_password': 'password',
            'new_password1': 'new_complex_password_123',
            'new_password2': 'new_complex_password_123'
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_complex_password_123'))

    def test_change_password_post_failure(self):
        """
        Test the POST request for the change password view with invalid data.
        Ensure the change password page reloads with the form and error
        messages.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('change_password'), {
            'old_password': 'password',
            'new_password1': 'new_complex_password_123',
            'new_password2': 'different_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        self.assertIsInstance(
            response.context['password_change_form'], PasswordChangeForm
        )

    def test_user_profile_sort_by_title(self):
        """
        Test the GET request for the user profile view with sorting by title.
        Ensure the issues are sorted correctly by title.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.get(
            reverse('profile'), {'sort_by': 'title', 'order': 'asc'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(
            response.context['page_obj'].object_list[0].title, 'Issue 1'
        )
        self.assertEqual(
            response.context['page_obj'].object_list[1].title, 'Issue 2'
        )

    def test_user_profile_pagination(self):
        """
        Test the GET request for the user profile view with pagination.
        Ensure the issues are paginated correctly.
        """
        self.client.login(username='testuser', password='password')
        for i in range(15):
            Issue.objects.create(
                title=f'Issue {i+3}', reporter=self.user, project=self.project
            )
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(len(response.context['page_obj']), 12)
