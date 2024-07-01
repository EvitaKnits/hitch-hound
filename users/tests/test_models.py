from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()

class UserModelTest(TestCase):

    def setUp(self):
        self.developer = User.objects.create_user(username='dev1', password='password123', role='developer')
        self.qa = User.objects.create_user(username='qa1', password='password123', role='quality_assurance')
        self.pm = User.objects.create_user(username='pm1', password='password123', role='product_manager')

    def test_create_user_with_role(self):
        """Test creating a user with a specific role"""
        self.assertEqual(self.developer.role, 'developer')
        self.assertEqual(self.qa.role, 'quality_assurance')
        self.assertEqual(self.pm.role, 'product_manager')

    def test_user_str_method(self):
        """Test the string representation of the User model"""
        self.assertEqual(str(self.developer), 'dev1')
        self.assertEqual(str(self.qa), 'qa1')
        self.assertEqual(str(self.pm), 'pm1')

    def test_developers_manager_method(self):
        """Test the UserManager developers method"""
        developers = User.objects.developers()
        self.assertIn(self.developer, developers)
        self.assertNotIn(self.qa, developers)
        self.assertNotIn(self.pm, developers)

    def test_quality_assurance_manager_method(self):
        """Test the UserManager quality_assurance method"""
        qas = User.objects.quality_assurance()
        self.assertIn(self.qa, qas)
        self.assertNotIn(self.developer, qas)
        self.assertNotIn(self.pm, qas)

    def test_product_managers_manager_method(self):
        """Test the UserManager product_managers method"""
        pms = User.objects.product_managers()
        self.assertIn(self.pm, pms)
        self.assertNotIn(self.developer, pms)
        self.assertNotIn(self.qa, pms)
