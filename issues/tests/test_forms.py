from django.test import TestCase
from issues.forms import IssueForm, CommentForm
from issues.models import Issue, Comment
from projects.models import Project
from users.models import User

class IssueFormTest(TestCase):
    """ Test case for the Issue Form """

    def setUp(self):
        """
        Set up the test data for Issue Form tests.
        Create instances of related models to be used in the form.
        """
        self.project = Project.objects.create(title='Test Project')
        self.developer = User.objects.create_user(username='developer', password='password', role='developer')
        self.quality_assurance = User.objects.create_user(username='qa', password='password', role='quality_assurance')
        self.product_manager = User.objects.create_user(username='pm', password='password', role='product_manager')

    def test_issue_form_valid_data(self):
        """
        Test Issue Form with valid data.
        The form should be valid.
        """
        form = IssueForm(data={
            'title': 'Test Issue',
            'description': 'Test Description',
            'severity': 2,  
            'project': self.project.id,
            'type': 'bug', 
            'developer': self.developer.id,
            'quality_assurance': self.quality_assurance.id,
            'product_manager': self.product_manager.id,
        })
        self.assertTrue(form.is_valid())

    def test_issue_form_no_data(self):
        """
        Test Issue Form with no data.
        The form should be invalid and contain errors.
        """
        form = IssueForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5) 

    def test_issue_form_missing_required_fields(self):
        """
        Test Issue Form with some required fields missing.
        The form should be invalid and contain errors for missing fields.
        """
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

    def test_issue_form_invalid_choices(self):
        """
        Test Issue Form with invalid choices for some fields.
        The form should be invalid and contain errors for invalid choices.
        """
        form = IssueForm(data={
            'title': 'Test Issue',
            'description': 'Test Description',
            'severity': 'invalid_choice',
            'project': self.project.id,
            'type': 'invalid_choice',
            'developer': self.developer.id,
            'quality_assurance': self.quality_assurance.id,
            'product_manager': self.product_manager.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('severity', form.errors)
        self.assertIn('type', form.errors)

class CommentFormTest(TestCase):
    """ Test case for the Comment Form """

    def setUp(self):
        """
        Set up the test data for Comment Form tests.
        Create instances of related models to be used in the form.
        """
        self.project = Project.objects.create(title='Test Project')
        self.reporter = User.objects.create_user(username='reporter', password='test')
        self.issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            project=self.project,
            reporter=self.reporter,
        )

    def test_comment_form_valid_data(self):
        """
        Test Comment Form with valid data.
        The form should be valid.
        """
        form = CommentForm(data={
            'comment_text': 'This is a comment.',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        """
        Test CommentForm with no data.
        The form should be invalid and contain errors.
        """
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('comment_text', form.errors)