from django.test import TestCase
from projects.forms import ProjectForm
from projects.models import Project

class ProjectFormTest(TestCase):
    """ Test case for the Project Form """
    def test_project_form_valid_data(self):
        """ Test that the Project Form is valid when provided valid data """
        form = ProjectForm(data={
            'title': 'Test Project',
        })
        self.assertTrue(form.is_valid())

    def test_project_form_no_data(self):
        """ Test that the Project Form is invalid when no data is provided """
        form = ProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)