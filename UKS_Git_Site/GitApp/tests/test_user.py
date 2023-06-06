
from django.test import TestCase, Client
from django.urls import reverse

from ..models import User
# # Create your tests here.


class LoginTestCase(TestCase):
    def setUp(self):
        self.wrong_user = {
            'username': 'testuser',
            'password': 'secret'}
        self.correct_user = {
            'username': 'user1',
            'password': 'user1'
        }
        User.objects.create(username="user1",password="user1",email="user1@user.com")
        User.objects.create(username="user2",password="user2",email="user2@user.com")

    def test_login_positive(self):
        response = self.client.post('/login/', self.correct_user, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_negative(self):
        response = self.client.post('/login/', self.wrong_user, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)