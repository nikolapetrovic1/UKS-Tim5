from django.test import TestCase, Client
from django.urls import reverse
from ..management.commands.fill_database import Command


class InitialTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # prepare test db for this test suite
        Command().handle()

    def setUp(self) -> None:
        # instantiate client for each test
        self.client = Client()

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_find_repository_successful(self):
        response = self.client.get('http://localhost:8083/2/')
        self.assertEqual(response.status_code, 200)

    def test_find_repository_unsuccessful(self):
        response = self.client.get('http://localhost:8083/99/')
        self.assertEqual(response.status_code, 404)
