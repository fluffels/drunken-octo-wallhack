import json

from django.http import HttpRequest
from django.http import HttpResponseForbidden
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
        url = "5nD-8euqNN4"
        data = '{{"url": "{}"}}'.format(url)
        response = self.client.post('/videos/', {'data': data})
        message = json.loads(response.content)
        self.assertEqual(message['status'], 0)

    def test_post_save(self):
        url = "5nD-8euqNN4"
        data = '{{"url": "{}"}}'.format(url)
        response = self.client.post('/videos/', {'data': data})
        message = json.loads(response.content)
        Video.objects.get(url=url)

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
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        v2 = Video()
        v2.url = "delete"
        v2.save()

        response = self.client.delete('/videos/{}/'.format(v2.id))
        message = json.loads(response.content)
        self.assertEqual(message['status'], 0)

        self.assertRaises(Video.DoesNotExist, Video.objects.get, url="delete")

