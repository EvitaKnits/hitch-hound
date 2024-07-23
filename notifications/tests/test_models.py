from django.test import TestCase
from django.utils import timezone
from issues.models import Issue
from projects.models import Project
from users.models import User
from notifications.models import Change

class ChangeModelTest(TestCase):
    """ Test case for the Change model """
    def setUp(self):
        """ Set up test data for the test case """
        self.user = User.objects.create(username='testuser', password='password')
        self.project = Project.objects.create(title='Test Project')  
        self.issue = Issue.objects.create(
            title='Test Issue', 
            description='Test description',
            project=self.project,  
            reporter=self.user  
        )

        self.change = Change.objects.create(
            issue=self.issue,
            user=self.user,
            field_changed='title',
            old_value='Old Title',
            new_value='New Title',
            changed_at=timezone.now()
        )

    def test_str_method(self):
        """
        Test the __str__ method of the Change model.
        This method should return a human-readable string representing the change.
        """
        expected_str = f'title changed from Old Title to New Title by {self.user}'
        self.assertEqual(str(self.change), expected_str)

    def test_field_choices(self):
        """
        Test that the field choices in the Change model include expected fields.
        """
        choices = [choice[0] for choice in Change.FIELD_CHOICES]
        self.assertIn('title', choices)
        self.assertIn('description', choices)
        self.assertIn('severity', choices)

