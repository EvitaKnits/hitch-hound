from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """ Test case for the User model """
    def setUp(self):
        """
        Set up the test data for User model tests.
        Create users with different roles for testing.
        """
        self.developer = User.objects.create_user(
            username='dev1', password='password123', role='developer', email='dev@hh.com'
        )
        self.qa = User.objects.create_user(
            username='qa1', password='password123', role='quality_assurance', email='qa@hh.com'
        )
        self.pm = User.objects.create_user(
            username='pm1', password='password123', role='product_manager', email='pm@hh.com'
        )

    def test_create_user_with_role(self):
        """
        Test creating a user with a specific role.
        Ensure that the role assigned to the user is correctly stored.
        """
        self.assertEqual(self.developer.role, 'developer')
        self.assertEqual(self.qa.role, 'quality_assurance')
        self.assertEqual(self.pm.role, 'product_manager')

    def test_user_str_method(self):
        """
        Test the string representation of the User model.
        Ensure that the string representation returns the username.
        """
        self.assertEqual(str(self.developer), 'dev1')
        self.assertEqual(str(self.qa), 'qa1')
        self.assertEqual(str(self.pm), 'pm1')

    def test_developers_manager_method(self):
        """
        Test the UserManager model's developers method.
        Ensure that the method returns users with the 'developer' role.
        """
        developers = User.objects.developers()
        self.assertIn(self.developer, developers)
        self.assertNotIn(self.qa, developers)
        self.assertNotIn(self.pm, developers)

    def test_quality_assurance_manager_method(self):
        """
        Test the UserManager model's quality_assurance method.
        Ensure that the method returns users with the 'quality_assurance' role.
        """
        qas = User.objects.quality_assurance()
        self.assertIn(self.qa, qas)
        self.assertNotIn(self.developer, qas)
        self.assertNotIn(self.pm, qas)

    def test_product_managers_manager_method(self):
        """
        Test the UserManager model's product_managers method.
        Ensure that the method returns users with the 'product_manager' role.
        """
        pms = User.objects.product_managers()
        self.assertIn(self.pm, pms)
        self.assertNotIn(self.developer, pms)
        self.assertNotIn(self.qa, pms)
