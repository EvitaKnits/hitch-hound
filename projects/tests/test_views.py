from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project
from issues.models import Issue
from projects.forms import ProjectForm

# Create your tests here.

User = get_user_model()

class ProjectViewsTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')
        
        # Create some projects
        self.project1 = Project.objects.create(title='Test Project 1')
        self.project2 = Project.objects.create(title='Test Project 2')
        
        # Create some issues
        self.issue1 = Issue.objects.create(
            title='Test Issue 1', 
            description='Description 1', 
            project=self.project1, 
            reporter=self.user,
            severity='high', 
            type='bug',       
            status='open'
        )
        self.issue2 = Issue.objects.create(
            title='Test Issue 2', 
            description='Description 2', 
            project=self.project1, 
            reporter=self.user,
            severity='medium',  
            type='other',       
            status='closed'    
        )

    def test_list_projects_view(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')
        self.assertIn('projects', response.context)
        self.assertEqual(len(response.context['projects']), 2)
        self.assertIn(self.issue1, response.context['projects'][0].latest_issues)
        
    def test_view_all_issues_view(self):
        response = self.client.get(reverse('view_all_issues', args=[self.project1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_issues.html')
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['page_obj']), 2)
        
    def test_create_project_view_get(self):
        response = self.client.get(reverse('create_project'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_project.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        
    def test_create_project_view_post(self):
        data = {
            'title': 'New Project',
        }
        response = self.client.post(reverse('create_project'), data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)  # Redirects to 'projects'
        self.assertTrue(Project.objects.filter(title='New Project').exists())
        
    def test_edit_project_view_get(self):
        response = self.client.get(reverse('edit_project', args=[self.project1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_project.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        
    def test_edit_project_view_post(self):
        data = {
            'title': 'Updated Project',
        }
        response = self.client.post(reverse('edit_project', args=[self.project1.id]), data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)  # Redirects to 'projects'
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.title, 'Updated Project')
        
    def test_delete_project_view(self):
        response = self.client.post(reverse('delete_project', args=[self.project1.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to 'projects'
        self.assertFalse(Project.objects.filter(id=self.project1.id).exists())