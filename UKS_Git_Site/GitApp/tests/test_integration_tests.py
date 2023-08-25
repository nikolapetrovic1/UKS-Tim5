from typing import assert_type
from django.http import response
from django.test import Client, TestCase
from django.urls import reverse

from ..management.commands.fill_database import Command
from ..models import Branch, DefaultBranch, PullRequest, Repository, User


# # Create your tests here.
class UserTestCase(TestCase):
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

    def test_register_ok(self):
        user = {
            "username": "dzonibro",
            "password1": "Nikolica123",
            "password2": "Nikolica123",
        }
        users_len = User.objects.count()
        self.client.post(reverse("user_register"), user)
        users_len_after = User.objects.count()
        self.assertNotEqual(users_len, users_len_after)

    def test_register_username_exists(self):
        user = {
            "username": "user1",
            "password1": "Nikolica123",
            "password2": "Nikolica123",
        }

        users_len = User.objects.count()
        self.client.post(reverse("user_register"), user)
        users_len_after = User.objects.count()
        self.assertEqual(users_len, users_len_after)

    def test_register_not_same_passwords(self):
        user = {
            "username": "user1",
            "password1": "Nikolica123",
            "password2": "ikolica123",
        }

        users_len = User.objects.count()
        self.client.post(reverse("user_register"), user)
        users_len_after = User.objects.count()
        self.assertEqual(users_len, users_len_after)

    def test_update_user_ok(self):
        user = {
            "username": "user1",
            "first_name": "Nikola",
        }
        self.client.login(username="user1", password="user1")
        user1 = User.objects.get(username="user1")
        self.assertNotEqual(user1.first_name, "Nikola")
        self.client.post(reverse("user_update"), user)
        user1 = User.objects.get(username="user1")
        self.assertEqual(user1.first_name, "Nikola")

    def test_change_password_not_same_password(self):
        data = {
            "old_password": "user1",
            "new_password1": "Nikola123",
            "new_password2": "ikola123",
        }
        logged_in = self.client.login(username="user1", password="user1")
        self.assertTrue(logged_in)
        self.client.post(reverse("change_password"), data)
        logged_in = self.client.login(username="user1", password="Nikola123")
        self.assertFalse(logged_in)

    def test_change_password_ok(self):
        data = {
            "old_password": "user1",
            "new_password1": "Nikola123",
            "new_password2": "Nikola123",
        }
        logged_in = self.client.login(username="user1", password="user1")
        self.assertTrue(logged_in)
        self.client.post(reverse("change_password"), data)
        logged_in = self.client.login(username="user1", password="user1")
        self.assertFalse(logged_in)
        logged_in = self.client.login(username="user1", password="Nikola123")
        self.assertTrue(logged_in)

    def test_delete_user_ok(self):
        self.assertTrue(User.objects.filter(username="user1").exists())
        logged_in = self.client.login(username="user1", password="user1")
        self.assertTrue(logged_in)
        self.client.post(reverse("delete_user"))
        self.assertFalse(User.objects.filter(username="user1").exists())


class RepositoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        c = Command()
        c.handle()

    def test_create_repository_ok(self):
        data = {"name": "uks-gitlight", "private": "PU"}
        logged_in = self.client.login(username="user2", password="user2")
        self.assertTrue(logged_in)
        repo_count = Repository.objects.count()
        self.client.post(reverse("create_repository"), data)
        self.assertNotEqual(repo_count, Repository.objects.count())

    def test_get_repository_ok(self):
        response = self.client.get(reverse("single_repository", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_edit_repository_error(self):
        data = {"name": "uks-tim5"}
        logged_in = self.client.login(username="user2", password="user2")
        self.assertTrue(logged_in)
        response = self.client.post(reverse("edit_repo", args=[1]), data)
        self.assertEqual(response.status_code, 404)

    def test_edit_repository_ok(self):
        data = {"name": "uks-tim5", "private": "PU"}
        logged_in = self.client.login(username="user1", password="user1")
        self.assertTrue(logged_in)
        self.client.post(reverse("edit_repo", args=[1]), data)
        repo = Repository.objects.get(id=1)
        self.assertEqual(data["name"], repo.name)

    def test_change_default_branch_ok(self):
        data = {"branch": 2}
        repo = Repository.objects.get(id=1)
        default_branch = DefaultBranch.objects.get(repository=repo)
        logged_in = self.client.login(username="user1", password="user1")
        self.assertTrue(logged_in)
        self.assertEqual(default_branch.branch.name, "main")
        self.client.post(reverse("select_default_branch", args=[1]), data)
        default_branch = DefaultBranch.objects.get(repository=repo)
        self.assertEqual(default_branch.branch.name, "develop")

    def test_create_branch_ok(self):
        data = {
            "name": "feat:test",
            "from_branch": 2,
        }
        branch_count = Branch.objects.count()
        logged_in = self.client.login(username="user1", password="user1")
        self.client.post(reverse("create_branch", args=[1]), data)
        self.assertNotEqual(branch_count, Branch.objects.count())

    def test_create_branch_already_exists_name(self):
        data = {
            "name": "main",
            "from_branch": 2,
        }
        repo = Repository.objects.filter(id=1)
        self.client.login(username="user1", password="user1")
        response = self.client.post(reverse("create_branch", args=[1]), data)
        self.assertEqual(response.status_code, 403)

    def test_create_pull_request_ok(self):
        data = {
            "source": 2,
            "target": 1,
        }
        pr_count = PullRequest.objects.count()
        self.client.login(username="user1", password="user1")
        self.client.post(reverse("create_pull_request", args=[1]), data)
        self.assertNotEqual(pr_count, PullRequest.objects.count())

    def test_delete_repository_404(self):
        logged_in = self.client.login(username="user2", password="user2")
        self.assertTrue(logged_in)
        response = self.client.get(reverse("delete_repo", args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_delete_repository_ok(self):
        logged_in = self.client.login(username="user1", password="user1")
        self.assertTrue(logged_in)
        self.client.get(reverse("delete_repo", args=[1]))
        self.assertFalse(Repository.objects.filter(id=1).exists())

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
