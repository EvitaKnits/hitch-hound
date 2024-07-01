from django.test import TestCase
from issues.forms import IssueForm
from issues.models import Issue
from projects.models import Project
from users.models import User

# Create your tests here.

class IssueFormTest(TestCase):
    def setUp(self):
        # Create instances of related models to be used in the form
        self.project = Project.objects.create(title="Test Project")
        self.developer = User.objects.create_user(username='developer', password='password', role='developer')
        self.quality_assurance = User.objects.create_user(username='qa', password='password', role='quality_assurance')
        self.product_manager = User.objects.create_user(username='pm', password='password', role='product_manager')

    def test_issue_form_valid_data(self):
        form = IssueForm(data={
            'title': 'Test Issue',
            'description': 'Test Description',
            'severity': 'high',  
            'project': self.project.id,
            'type': 'bug', 
            'status': 'open',  
            'developer': self.developer.id,
            'quality_assurance': self.quality_assurance.id,
            'product_manager': self.product_manager.id,
        })
        print(form.errors)  # Print form errors to debug
        self.assertTrue(form.is_valid())

    def test_issue_form_no_data(self):
        form = IssueForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6) 

    def test_issue_form_missing_required_fields(self):
        form = IssueForm(data={
            'title': '',
            'description': 'Test Description',
            'severity': '',
            'project': self.project.id,
            'type': 'bug',
            'status': 'open',
            'developer': self.developer.id,
            'quality_assurance': self.quality_assurance.id,
            'product_manager': self.product_manager.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('severity', form.errors)