import json

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.views.generic.base import TemplateView

from .models import Video

def error(status, message):
    """Return an error messsage formatted as a JSON object."""

    error = {"status": status, "message": message}
    return HttpResponse(json.dumps(error))

def format_video(video):
    """Format a specific video in JSON."""
    return {"id": video.id, "url": video.url, "title": video.title, "description": video.description}

def success(message=""):
    """Return a success message formatted as a JSON object."""

    success = {"status": 0, "message": message}
    return HttpResponse(json.dumps(success))

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context

class VideoAPIView(View):
    """Implements GET and POST for the video API described in the README."""
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""

        if ("data" not in request.POST):
            return error(1, ('Please send a valid JSON object in the '
                             '"data" field of the POST request.'))
        else:
            json_data = request.POST["data"]

            try:
                data = json.loads(json_data)
            except Exception as e:
                return error(2, "Error while parsing JSON string '{}': {}".
                                 format(json_data, e))
            if "url" in data:
                video = Video()
                video.url = data["url"]
                if "description" in data:
                    video.description = data["description"]
                video.fetch_details()
                video.save()
                return success(video.id)
            else:
                return error(3, "No url found in JSON string '{}'.".
                                 format(json_data))

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""

        videos = Video.objects.all()
        data = [format_video(video) for video in videos]
        response = json.dumps(data)

        return HttpResponse(response)

class IndividualVideoAPIView(View):
    """Implements DELETE and GET for individual videos."""

    def delete(self, request, id):
        v = Video.objects.get(id=id)
        v.delete()
        return success()

    def get(self, request, id):
        v = Video.objects.get(id=id)
        return HttpResponse(json.dumps(format_video(v)))

