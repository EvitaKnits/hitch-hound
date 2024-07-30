from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from issues.models import Issue, Comment
from projects.models import Project
from issues.forms import IssueForm, CommentForm

User = get_user_model()


class IssueViewsTest(TestCase):
    """ Test case for the views related to the Issue model """
    def setUp(self):
        """ Set up the test data for Issue views tests """
        # Create a user and log them in
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Create a project
        self.project = Project.objects.create(title='Test Project')

        # Create some issues
        self.issue1 = Issue.objects.create(
            title='Test Issue 1',
            description='Description 1',
            project=self.project,
            reporter=self.user,
            severity=2,
            type='bug',
            status='open'
        )
        self.issue2 = Issue.objects.create(
            title='Test Issue 2',
            description='Description 2',
            project=self.project,
            reporter=self.user,
            severity=3,
            type='other',
            status='closed'
        )

    def test_list_issues_view(self):
        """ Test the home page: list all issues view """
        response = self.client.get(reverse('issues'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issues.html')
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['page_obj']), 2)

    def test_list_issues_sorting(self):
        """ Test the sorting of issues in the list issues view """
        response = self.client.get(
            reverse('issues') + '?sort_by=title&order=desc'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issues.html')
        self.assertIn('page_obj', response.context)
        issues = list(response.context['page_obj'])
        self.assertEqual(issues[0], self.issue2)
        self.assertEqual(issues[1], self.issue1)

    def test_issue_detail_view(self):
        """ Test the issue detail view """
        response = self.client.get(
            reverse('issue_detail', args=[self.issue1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issue_detail.html')
        self.assertEqual(response.context['issue'], self.issue1)

    def test_create_issue_view_get(self):
        """ Test the create issue view (GET request) """
        response = self.client.get(reverse('create_issue'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_issue.html')
        self.assertIsInstance(response.context['form'], IssueForm)

    def test_create_issue_view_post(self):
        """ Test the create issue view (POST request) """
        data = {
            'title': 'New Issue',
            'description': 'New Issue Description',
            'project': self.project.id,
            'severity': 2,
            'type': 'bug',
            'status': 'open'
        }
        response = self.client.post(reverse('create_issue'), data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Issue.objects.filter(title='New Issue').exists())

    def test_edit_issue_view_get(self):
        """ Test the edit issue view (GET request) """
        response = self.client.get(
            reverse('edit_issue', args=[self.issue1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_issue.html')
        self.assertIsInstance(response.context['form'], IssueForm)

    def test_edit_issue_view_post(self):
        """ Test the edit issue view (POST request) """
        data = {
            'title': 'Updated Issue',
            'description': 'Updated Description',
            'project': self.project.id,
            'severity': 2,
            'type': 'bug',
            'status': 'open'
        }
        response = self.client.post(
            reverse('edit_issue', args=[self.issue1.id]), data
        )
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.issue1.refresh_from_db()
        self.assertEqual(self.issue1.title, 'Updated Issue')

    def test_delete_issue_view(self):
        """ Test the delete issue view """
        response = self.client.post(
            reverse('delete_issue', args=[self.issue1.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Issue.objects.filter(id=self.issue1.id).exists())

    def test_add_comment_view(self):
        """ Test the add comment view """
        data = {
            'comment_text': 'This is a test comment.',
        }
        response = self.client.post(
            reverse('add_comment', args=[self.issue1.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(
                comment_text='This is a test comment.', issue=self.issue1
            ).exists()
        )

    def test_add_comment_view_invalid(self):
        """ Test the add comment view with invalid data """
        data = {
            'comment_text': '',
        }
        response = self.client.post(
            reverse('add_comment', args=[self.issue1.id]), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CommentForm)
        self.assertFalse(
            Comment.objects.filter(comment_text='', issue=self.issue1).exists()
        )
