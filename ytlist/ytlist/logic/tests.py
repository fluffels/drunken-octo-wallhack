import json

from django.http import HttpRequest
from django.test import TestCase
from django.test import Client

from .views import VideoAPIView

class VideoAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_success(self):
        response = self.client.post('/videos/', {'data': '{"url": "test"}'})
        message = json.loads(response.content)
        self.assertEqual(message['status'], 0)

    def test_post_error(self):
        response = self.client.post('/videos/')
        message = json.loads(response.content)
        self.assertEqual(message['status'], 1)

    def test_parse_error(self):
        response = self.client.post('/videos/', {'data': '{"test"}'})
        message = json.loads(response.content)
        self.assertEqual(message['status'], 2)

