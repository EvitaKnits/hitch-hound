from django.test import TestCase
from projects.forms import ProjectForm
from projects.models import Project

# Create your tests here.

class ProjectFormTest(TestCase):
    def test_project_form_valid_data(self):
        form = ProjectForm(data={
            'title': 'Test Project',
        })
        self.assertTrue(form.is_valid())

    def test_project_form_no_data(self):
        form = ProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)