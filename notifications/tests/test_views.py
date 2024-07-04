from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from issues.models import Issue
from projects.models import Project
from users.models import User
from notifications.models import Change

class ChangeHistoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser', password='password')
        self.project = Project.objects.create(title='Test Project')  # Create a Project instance
        self.issue1 = Issue.objects.create(
            title='Test Issue 1', 
            description='Test description 1',
            project=self.project,  # Associate the Issue with the Project
            reporter=self.user  # Set the reporter
        )
        self.issue2 = Issue.objects.create(
            title='Test Issue 2', 
            description='Test description 2',
            project=self.project,  # Associate the Issue with the Project
            reporter=self.user  # Set the reporter
        )

        # Create Change instances
        self.change1 = Change.objects.create(
            issue=self.issue1,
            user=self.user,
            field_changed='title',
            old_value='Old Title 1',
            new_value='New Title 1',
            changed_at=timezone.now()
        )
        self.change2 = Change.objects.create(
            issue=self.issue1,
            user=self.user,
            field_changed='description',
            old_value='Old Description',
            new_value='New Description',
            changed_at=timezone.now() - timezone.timedelta(days=1)
        )

    def test_change_history_view_issue_specific(self):
        response = self.client.get(reverse('issue_change_history', args=[self.issue1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_history.html')
        self.assertIn(self.change1, response.context['changes'])
        self.assertIn(self.change2, response.context['changes'])
        self.assertGreater(response.context['changes'][0].changed_at, response.context['changes'][1].changed_at)

    def test_change_history_view_no_changes(self):
        response = self.client.get(reverse('issue_change_history', args=[self.issue2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_history.html')
        self.assertQuerysetEqual(response.context['changes'], [])
