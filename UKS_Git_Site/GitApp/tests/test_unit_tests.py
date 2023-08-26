from django.test import TestCase, Client
from django.urls import reverse
from django.db.utils import DataError
from ..utils import milestone_progress
from ..models import (
    IssueState,
    Repository,
    User,
    Milestone,
    Issue,
    Branch,
    PullRequest,
    State,
    User,
    Task,
    Comment,
)
from ..management.commands.fill_database import Command


# # Create your tests here.
class UnitTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        c = Command()
        c.handle()

    def test_milestone_progress(self):
        milestone = Milestone.objects.get(id=1)
        progress = milestone_progress(milestone)
        self.assertEqual(progress.percent, 50)

    def test_milestone_update_progress(self):
        milestone = Milestone.objects.get(id=1)
        progress = milestone_progress(milestone)
        self.assertEqual(progress.percent, 50)
        open_issue = Issue.objects.filter(
            milestone=milestone, state=IssueState.OPEN
        ).first()
        open_issue.state = IssueState.CLOSED
        open_issue.save()

        milestone = Milestone.objects.get(id=1)
        progress = milestone_progress(milestone)
        self.assertEqual(progress.percent, 100)

    def test_get_milestone(self):
        milestone = Milestone.objects.all()
        self.assertEqual(len(milestone), 1)
        self.assertEqual(milestone[0].title, "test milestone")

    def test_create_milestone(self):
        repo = Repository.objects.get(id=1)
        milestone = Milestone(
            title="pera",
            repository=repo,
            due_date="2023-12-28",
            description="this is milestone",
        )
        milestone.save()
        self.assertEqual(milestone.id, 2)


class PullRequestUnitTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "user1", "user1@mailinator.com", "user1", company="FTN"
        )
        self.repo = Repository.objects.create(name="test_repo", lead=self.user)
        self.branch_a = Branch.objects.create(name="branch_a", repository=self.repo)
        self.branch_b = Branch.objects.create(name="branch_b", repository=self.repo)
        self.pull_request = PullRequest.objects.create(
            target=self.branch_a,
            source=self.branch_b,
            creator=self.user,
            repository=self.repo,
        )

    def test_pull_request_creation(self):
        self.assertEqual(self.pull_request.state, State.OPEN)
        self.assertEqual(self.pull_request.target, self.branch_a)
        self.assertEqual(self.pull_request.source, self.branch_b)

    def test_pull_request_state_default(self):
        new_pr = PullRequest.objects.create(
            target=self.branch_a,
            source=self.branch_b,
            creator=self.user,
            repository=self.repo,
        )
        self.assertEqual(new_pr.state, State.OPEN)

    def test_pull_request_state_choices(self):
        with self.assertRaises(DataError):
            invalid_pr = PullRequest.objects.create(
                state="invalid_state",
                target=self.branch_a,
                source=self.branch_b,
                creator=self.user,
                repository=self.repo,
            )


class IssueUnitTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "user1", "user1@mailinator.com", "user1", company="FTN"
        )
        self.repo = Repository.objects.create(name="test_repo", lead=self.user)
        self.issue = Issue.objects.create(
            title="Example Issue",
            description="This is an example issue",
            creator=self.user,
            repository=self.repo,
        )

    def test_issue_creation(self):
        self.assertEqual(self.issue.title, "Example Issue")
        self.assertEqual(self.issue.description, "This is an example issue")
        self.assertEqual(self.issue.state, IssueState.OPEN)
        self.assertEqual(self.issue.labels.count(), 0)  # No labels added in this test

    def test_issue_date_created(self):
        self.assertIsNotNone(self.issue.date_created)

    def test_issue_state_default(self):
        new_issue = Issue.objects.create(
            title="New Issue",
            description="This is an example issue",
            creator=self.user,
            repository=self.repo,
        )
        self.assertEqual(new_issue.state, IssueState.OPEN)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.repo = Repository.objects.create(name="test_repo", lead=self.user)
        self.task = Task.objects.create(repository=self.repo, creator=self.user)
        self.comment = Comment.objects.create(
            created_by=self.user, content="This is a test comment", task=self.task
        )

    def test_created_by_field(self):
        self.assertEqual(self.comment.created_by, self.user)

    def test_content_field(self):
        self.assertEqual(self.comment.content, "This is a test comment")

    def test_delete_task_cascade(self):
        self.task.delete()
        # Check if the comment is deleted when the related task is deleted
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=self.comment.pk)
