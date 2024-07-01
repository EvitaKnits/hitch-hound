from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from issues.models import Issue
from projects.models import Project
from issues.forms import IssueForm

# Create your tests here.
User = get_user_model()

class IssueViewsTest(TestCase):
    
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
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
            severity='high',
            type='bug',
            status='open'
        )
        self.issue2 = Issue.objects.create(
            title='Test Issue 2', 
            description='Description 2', 
            project=self.project, 
            reporter=self.user,
            severity='medium',
            type='other',
            status='closed'
        )
        
    def test_list_issues_view(self):
        response = self.client.get(reverse('issues'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issues.html')
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['page_obj']), 2)
        
    def test_issue_detail_view(self):
        response = self.client.get(reverse('issue_detail', args=[self.issue1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'issue_detail.html')
        self.assertEqual(response.context['issue'], self.issue1)
        
    def test_create_issue_view_get(self):
        response = self.client.get(reverse('create_issue'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_issue.html')
        self.assertIsInstance(response.context['form'], IssueForm)
        
    def test_create_issue_view_post(self):
        data = {
            'title': 'New Issue',
            'description': 'New Issue Description',
            'project': self.project.id,
            'severity': 'high',
            'type': 'bug',
            'status': 'open'
        }
        response = self.client.post(reverse('create_issue'), data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)  # Redirects to 'issues'
        self.assertTrue(Issue.objects.filter(title='New Issue').exists())
        
    def test_edit_issue_view_get(self):
        response = self.client.get(reverse('edit_issue', args=[self.issue1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_issue.html')
        self.assertIsInstance(response.context['form'], IssueForm)
        
    def test_edit_issue_view_post(self):
        data = {
            'title': 'Updated Issue',
            'description': 'Updated Description',
            'project': self.project.id,
            'severity': 'high',
            'type': 'bug',
            'status': 'open'
        }
        response = self.client.post(reverse('edit_issue', args=[self.issue1.id]), data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)  # Redirects to 'issue_detail'
        self.issue1.refresh_from_db()
        self.assertEqual(self.issue1.title, 'Updated Issue')
        
    def test_delete_issue_view(self):
        response = self.client.post(reverse('delete_issue', args=[self.issue1.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to 'issues'
        self.assertFalse(Issue.objects.filter(id=self.issue1.id).exists())