from django.test import TestCase
from django.urls import reverse

from .models import User
# # Create your tests here.


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="user1",password="user1",email="user1@user.com")
        User.objects.create(username="user2",password="user2",email="user2@user.com")

    def test_login_positive(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)