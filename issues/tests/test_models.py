from django.test import TestCase
from django.contrib.auth import get_user_model
from issues.models import Issue, UserIssue, Comment
from projects.models import Project
from django.core.exceptions import ValidationError

User = get_user_model()


class IssueModelTest(TestCase):
    """ Test case for the Issue model """
    def setUp(self):
        """ Set up the test data for Issue model tests """
        self.project = Project.objects.create(title='Test Project')
        self.reporter = User.objects.create_user(
            username='reporter', password='test'
        )
        self.developer = User.objects.create_user(
            username='developer', password='test', role='developer'
        )
        self.qa = User.objects.create_user(
            username='qa', password='test', role='quality_assurance'
        )
        self.pm = User.objects.create_user(
            username='pm', password='test', role='product_manager'
        )
        self.superuser = User.objects.create_superuser(
            username='superuser', password='test123'
        )

        self.issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            severity=4,
            project=self.project,
            type='bug',
            status='open',
            reporter=self.reporter
        )

    def test_create_issue(self):
        """ Test creating an Issue instance with valid data """
        issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            severity=2,
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
        self.assertEqual(issue.severity, 2)
        self.assertEqual(issue.project, self.project)
        self.assertEqual(issue.type, 'bug')
        self.assertEqual(issue.status, 'open')
        self.assertEqual(issue.reporter, self.reporter)
        self.assertEqual(issue.developer, self.developer)
        self.assertEqual(issue.quality_assurance, self.qa)
        self.assertEqual(issue.product_manager, self.pm)

    def test_issue_default_values(self):
        """ Test the default values for an Issue instance """
        issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            project=self.project,
            reporter=self.reporter,
        )
        self.assertEqual(issue.severity, 4)
        self.assertEqual(issue.type, 'bug')
        self.assertEqual(issue.status, 'open')
        self.assertIsNone(issue.developer)
        self.assertIsNone(issue.quality_assurance)
        self.assertIsNone(issue.product_manager)

    def test_missing_required_field(self):
        """
        Test creating an Issue instance with a missing required field (title).
        Should raise a ValidationError.
        """
        with self.assertRaises(ValidationError):
            issue = Issue(
                description='This is a test issue',
                project=self.project,
                reporter=self.reporter,
            )
            issue.full_clean()

    def test_title_max_length(self):
        """
        Test the maximum length of the title field.
        Should raise a ValidationError because max length is exceeded.
        """
        with self.assertRaises(ValidationError):
            issue = Issue(
                title='T' * 256,
                description='This is a test issue',
                project=self.project,
                reporter=self.reporter,
            )
            issue.full_clean()

    def test_related_objects_deletion(self):
        """
        Test the cascading deletion of related objects.
        Deleting an Issue should delete related Comments.
        """
        issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            project=self.project,
            reporter=self.reporter,
        )
        comment = Comment.objects.create(
            comment_text='This is a comment',
            user=self.reporter,
            issue=issue,
        )
        issue_id = issue.id
        comment_id = comment.id
        issue.delete()
        self.assertFalse(Issue.objects.filter(id=issue_id).exists())
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

    # Permission system tests

    def test_can_user_update_status(self):
        """
        Test the permission system for updating the status of an Issue.
        Different roles have different permissions for changing status.
        """
    # Developer can only move to 'in_progress'
    self.assertTrue(
        self.issue.can_user_update_status(self.developer, 'in_progress')
    )
    self.assertFalse(
        self.issue.can_user_update_status(self.developer, 'closed')
    )

    # QA can only move to 'testing'
    self.assertTrue(
        self.issue.can_user_update_status(self.qa, 'testing')
    )
    self.assertFalse(
        self.issue.can_user_update_status(self.qa, 'approved')
    )

    # Product Manager can move to 'approved', 'closed', and 'cancelled'
    self.assertTrue(
        self.issue.can_user_update_status(self.pm, 'approved')
    )
    self.assertTrue(
        self.issue.can_user_update_status(self.pm, 'closed')
    )
    self.assertTrue(
        self.issue.can_user_update_status(self.pm, 'cancelled')
    )
    self.assertFalse(
        self.issue.can_user_update_status(self.pm, 'testing')
    )

    # Superuser can move to any status
    self.assertTrue(
        self.issue.can_user_update_status(self.superuser, 'closed')
    )
    self.assertTrue(
        self.issue.can_user_update_status(self.superuser, 'in_progress')
    )

    def test_save_method_permissions(self):
        """
        Test the custom save method for permissions when updating status
        """
        self.issue.status = 'in_progress'
        self.issue.save(user=self.developer)
        self.assertEqual(self.issue.status, 'in_progress')

        self.issue.status = 'closed'
        success = self.issue.save(user=self.developer)
        self.assertFalse(success)
        self.issue.refresh_from_db()
        self.assertNotEqual(self.issue.status, 'closed')


class CommentModelTest(TestCase):
    """ Test case for the Comment model """

    def setUp(self):
        """ Set up the test data for Comment model tests """
        self.project = Project.objects.create(title='Test Project')
        self.reporter = User.objects.create_user(
            username='reporter', password='test'
        )
        self.user = User.objects.create_user(
            username='commenter', password='test'
        )
        self.issue = Issue.objects.create(
            title='Test Issue',
            description='This is a test issue',
            project=self.project,
            reporter=self.reporter,
        )

    def test_create_comment(self):
        """ Test creating a Comment instance with valid data """
        comment = Comment.objects.create(
            comment_text='This is a test comment',
            user=self.user,
            issue=self.issue
        )
        self.assertEqual(comment.comment_text, 'This is a test comment')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.issue, self.issue)
        self.assertIsNotNone(comment.commented_at)

    def test_comment_text_cannot_be_blank(self):
        """
        Test that the comment_text field cannot be blank.
        Should raise a ValidationError.
        """
        comment = Comment(comment_text='', user=self.user, issue=self.issue)
        with self.assertRaises(ValidationError):
            comment.full_clean()
            comment.save()

    def test_str_method(self):
        """
        Test the __str__ method of the Comment model.
        Should return the first 20 characters of the comment_text.
        """
        comment = Comment.objects.create(
            comment_text='This is a comment that is longer than 20 characters',
            user=self.reporter,
            issue=self.issue,
        )
        self.assertEqual(str(comment), 'This is a comment th')
