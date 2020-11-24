from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Comment, Collaborator, Decision
from rest_framework.test import APIClient

Writer = get_user_model()


class WriterTestCase(TestCase):

    def setUp(self):
        self.writer = Writer.objects.create_user(email='test@email.com', first_name='test_first', last_name='test_last', password='123456')

    def test_writer_created(self):
        writer = Writer.objects.get(email='test@email.com')
        self.assertEqual(writer.email, 'test@email.com')

    def get_client(self):
        client = APIClient
        self.client.login(username=self.writer.email, password='123456')
        return client

    def test_api_login(self):
      self.login = self.client.login(email='test@email.com', password='123456')
      self.response = self.client.post('/accounts/session/',
                                       {'email': 'test@email.com', 'password': '123456'}, format='json')
      self.assertEqual(self.response.status_code, 200)

