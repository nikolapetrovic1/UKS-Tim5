from django.test import TestCase, Client
from django.urls import reverse

from ..utils import milestone_progress, reset_sequence
from ..models import IssueState, Repository, User, Milestone, Issue
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
