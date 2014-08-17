import json

from django.http import HttpRequest
from django.test import TestCase
from django.test import Client

from .models import Video
from .views import VideoAPIView

class VideoAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

        v = Video()
        v.url = "retrieve"
        v.save()

    def test_retrieve(self):
        v = Video.objects.get(url="retrieve")

    def test_post_success(self):
        response = self.client.post('/videos/', {'data': '{"url": "test"}'})
        message = json.loads(response.content)
        self.assertEqual(message['status'], 0)

    def test_post_save(self):
        response = self.client.post('/videos/', {'data': '{"url": "test2"}'})
        message = json.loads(response.content)
        Video.objects.get(url="test2")

    def test_post_save_fail(self):
        self.assertRaises(Video.DoesNotExist, Video.objects.get, url="none")

    def test_post_error(self):
        response = self.client.post('/videos/')
        message = json.loads(response.content)
        self.assertEqual(message['status'], 1)

    def test_parse_error(self):
        response = self.client.post('/videos/', {'data': '{"test"}'})
        message = json.loads(response.content)
        self.assertEqual(message['status'], 2)

    def test_no_url(self):
        response = self.client.post('/videos/',
                                    {'data': '{"description": "test"}'})
        message = json.loads(response.content)
        self.assertEqual(message['status'], 3)

    def test_get(self):
        response = self.client.get('/videos/')
        self.assertEqual(response.content,
                         '[{"url": "retrieve", "description": ""}]')

