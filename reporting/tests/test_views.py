from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from issues.models import Issue, UserIssue
from notifications.models import Change
from projects.models import Project
from users.models import User


class ViewsTestCase(TestCase):
    """ Test case for the views related to the Reports application """
    def setUp(self):
        """
        Set up the test environment for each test case.
        This includes creating a test client, user, project, issue, user issue,
        and change.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.client.login(username='testuser', password='12345')

        self.project = Project.objects.create(title='Test Project')
        self.issue = Issue.objects.create(
            title='Test Issue',
            status='Open',
            project=self.project,
            reporter=self.user
        )
        self.user_issue = UserIssue.objects.create(
            user=self.user, issue=self.issue
        )
        self.change = Change.objects.create(
            issue=self.issue, user=self.user, changed_at=timezone.now()
        )

    def test_issue_listing_by_status(self):
        """
        Test the Issue Listing by Status report view to ensure it returns the
        correct template and context data.
        """
        response = self.client.get(reverse('issue_listing_by_status'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issue_listing_by_status.html')
        self.assertIn('issues', response.context)
        self.assertIn('status_choices', response.context)
        self.assertIn('project_choices', response.context)

    def test_issue_listing_by_assignee(self):
        """
        Test the Issue Listing by Assignee report view to ensure it returns the
        correct template and context data.
        """
        response = self.client.get(reverse('issue_listing_by_assignee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issue_listing_by_assignee.html')
        self.assertIn('issues', response.context)
        self.assertIn('user_choices', response.context)

    def test_issue_status_summary(self):
        """
        Test the Issue Status Summary report view to ensure it returns the
        correct template and context data.
        """
        response = self.client.get(reverse('issue_status_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issue_status_summary.html')
        self.assertIn('labels', response.context)
        self.assertIn('data', response.context)
        self.assertIn('project_choices', response.context)

    def test_issue_severity_summary(self):
        """
        Test the Issue Severity Summary report view to ensure it returns the
        correct template and context data.
        """
        response = self.client.get(reverse('issue_severity_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issue_severity_summary.html')
        self.assertIn('labels', response.context)
        self.assertIn('data', response.context)
        self.assertIn('project_choices', response.context)
