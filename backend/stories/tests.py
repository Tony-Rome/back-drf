from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Story
from rest_framework.test import APIClient

Writer = get_user_model()


class TestStory(TestCase):

    def setUp(self):
        self.writer = Writer.objects.create_user(email='test@email.com', first_name='first_test', last_name='last_test', password='123456')
        Story.objects.create(writer=self.writer, title='Test title', content='Content test')

    def get_client(self):
        client = APIClient()
        client.login(email='test@email', password='123456')
        return client

    def test_story_list(self):
        client = self.get_client()
        response = client.get("/stories/all-stories/")
        self.assertEqual(len(response.json()), 1)
