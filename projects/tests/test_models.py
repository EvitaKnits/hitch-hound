from django.test import TestCase
from projects.models import Project
from django.core.exceptions import ValidationError

# Create your tests here.

class ProjectModelTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(title='Test Project')

    def test_create_project(self):
        """Test creating a Project with a title"""
        self.assertEqual(self.project.title, 'Test Project')

    def test_str_method(self):
        """Test the string representation of the Project model"""
        self.assertEqual(str(self.project), 'Test Project')

    def test_project_title_cannot_be_blank(self):
        """Test that a project cannot have a blank title"""
        project = Project(title='')
        with self.assertRaises(ValidationError):
            project.full_clean() 