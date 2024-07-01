from django.test import TestCase
from django.contrib.auth import get_user_model
from issues.models import Issue, UserIssue
from projects.models import Project
from django.core.exceptions import ValidationError

# Create your tests here.

User = get_user_model()

class IssueModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(title='Test Project')
        self.reporter = User.objects.create_user(username='reporter', password='test')
        self.developer = User.objects.create_user(username='developer', password='test', role='developer')
        self.qa = User.objects.create_user(username='qa', password='test', role='quality_assurance')
        self.pm = User.objects.create_user(username='pm', password='test', role='product_manager')

    def test_create_issue(self):
        issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            severity='high',
            project=self.project,
            type='bug',
            status='open',
            reporter=self.reporter,
            developer=self.developer,
            quality_assurance=self.qa,
            product_manager=self.pm,
        )
        self.assertEqual(issue.title, 'Test Issue')
        self.assertEqual(issue.description, 'This is a test issue')
        self.assertEqual(issue.severity, 'high')
        self.assertEqual(issue.project, self.project)
        self.assertEqual(issue.type, 'bug')
        self.assertEqual(issue.status, 'open')
        self.assertEqual(issue.reporter, self.reporter)
        self.assertEqual(issue.developer, self.developer)
        self.assertEqual(issue.quality_assurance, self.qa)
        self.assertEqual(issue.product_manager, self.pm)

    def test_issue_default_values(self):
        issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            project=self.project,
            reporter=self.reporter,
        )
        self.assertEqual(issue.severity, 'low')
        self.assertEqual(issue.type, 'bug')
        self.assertEqual(issue.status, 'open')
        self.assertIsNone(issue.developer)
        self.assertIsNone(issue.quality_assurance)
        self.assertIsNone(issue.product_manager)

    def test_missing_required_field(self):
        with self.assertRaises(ValidationError):
            issue = Issue(
                description='This is a test issue',  # Missing title
                project=self.project,
                reporter=self.reporter,
            )
            issue.full_clean()

    def test_title_max_length(self):
        with self.assertRaises(ValidationError):
            issue = Issue(
                title='T' * 256,  # Title exceeds max length
                description='This is a test issue',
                project=self.project,
                reporter=self.reporter,
            )
            issue.full_clean()

class UserIssueModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(title='Test Project')
        self.reporter = User.objects.create_user(username='reporter', password='test')
        self.issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            project=self.project,
            reporter=self.reporter,
        )
        self.user = User.objects.create_user(username='developer', password='test')

    def test_create_user_issue(self):
        user_issue = UserIssue.objects.create(
            user=self.user,
            issue=self.issue,
            role='developer',
        )
        self.assertEqual(user_issue.user, self.user)
        self.assertEqual(user_issue.issue, self.issue)
        self.assertEqual(user_issue.role, 'developer')

    def test_unique_together_constraint(self):
        # Create a UserIssue instance
        UserIssue.objects.create(
            user=self.user,
            issue=self.issue,
            role='developer',
        )
        # Attempt to create a duplicate UserIssue instance
        with self.assertRaises(ValidationError):
            duplicate_user_issue = UserIssue(
                user=self.user,
                issue=self.issue,
                role='developer',
            )
            duplicate_user_issue.full_clean()  
