from django.test import TestCase, Client
from django.urls import reverse

from ..models import User
from ..management.commands.fill_database import Command


# # Create your tests here.
class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        c = Command()
        c.handle()

    def test_login_positive(self):
        logged_in = self.client.login(username="user1", password="user1")
        self.assertTrue(logged_in)

    def test_login_negative(self):
        logged_in = self.client.login(username="user2", password="user1")
        self.assertFalse(logged_in)

    def test_get_repository_ok(self):
        response = self.client.get(reverse("single_repository", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_get_private_repository_ok(self):
        self.client.login(username="user2", password="user2")
        response = self.client.get(reverse("single_repository", args=[2]))
        self.assertEqual(response.status_code, 200)

    def test_get_private_repository_404(self):
        response = self.client.get(reverse("single_repository", args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_get_repository_404(self):
        response = self.client.get(reverse("single_repository", args=[99]))
        self.assertEqual(response.status_code, 404)


class IssueTests(TestCase):
    pass


class MilestoneTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        c = Command()
        c.handle()

    def test_get_one_repo_milestone(self):
        response = self.client.get(reverse("milestone_page", args=[1, 1]))
        self.assertEqual(response.status_code, 200)

    def test_get_one_repo_milestone_wrong_repo(self):
        response = self.client.get(reverse("milestone_page", args=[2, 1]))
        self.assertEqual(response.status_code, 404)

    def test_get_one_repo_milestone_wrong_milestone(self):
        response = self.client.get(reverse("milestone_page", args=[1, 99]))
        self.assertEqual(response.status_code, 404)
