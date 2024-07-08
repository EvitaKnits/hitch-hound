from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from issues.models import Issue, UserIssue
from projects.models import Project
from users.models import User
from notifications.models import Change

class ListNotificationsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.last_visited_notifications = timezone.now() - timezone.timedelta(days=2)
        self.user.save()

        # Create another user to make changes
        self.other_user = User.objects.create_user(username='otheruser', password='12345')

        self.project = Project.objects.create(title='Test Project')
        self.issue = Issue.objects.create(title='Test Issue', reporter=self.user, project=self.project)
        self.user_issue = UserIssue.objects.create(user=self.user, issue=self.issue)

        # Create changes made by the other user
        self.change1 = Change.objects.create(issue=self.issue, user=self.other_user, field_changed='status', old_value='open', new_value='closed', changed_at=timezone.now() - timezone.timedelta(days=1))
        self.change2 = Change.objects.create(issue=self.issue, user=self.other_user, field_changed='priority', old_value='low', new_value='high', changed_at=timezone.now() - timezone.timedelta(hours=1))

        self.url = reverse('notifications')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/accounts/login/?next=/notifications/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications.html')

    def test_last_visited_notifications_updated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.user.refresh_from_db()
        self.assertAlmostEqual(self.user.last_visited_notifications, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_notifications_list(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)

        # Check that the correct Change objects are included
        self.assertIn(self.change1, response.context['page_obj'].object_list)
        self.assertIn(self.change2, response.context['page_obj'].object_list)

class ChangeHistoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.project = Project.objects.create(title='Test Project')
        self.issue1 = Issue.objects.create(
            title='Test Issue 1', 
            description='Test description 1',
            project=self.project,
            reporter=self.user
        )
        self.issue2 = Issue.objects.create(
            title='Test Issue 2', 
            description='Test description 2',
            project=self.project,
            reporter=self.user
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

        # Log in the user
        self.client.login(username='testuser', password='password')

    def test_change_history_view_issue(self):
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
