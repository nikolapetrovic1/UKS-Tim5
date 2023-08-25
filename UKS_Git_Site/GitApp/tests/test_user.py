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

    def test_get_repository_404(self):
        response = self.client.get(reverse("single_repository", args=[99]))
        self.assertEqual(response.status_code, 404)
