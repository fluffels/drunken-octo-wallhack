import json

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.views.generic.base import TemplateView

from .models import Video

def error(status, message):
    """Return an error messsage formatted as a JSON object."""

    error = {"status": status, "message": message}
    return HttpResponse(json.dumps(error))

def success():
    """Return a success message formatted as a JSON object."""

    success = {"status": 0, "message": ""}
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
                video.save()
                return success()
            else:
                return error(3, "No url found in JSON string '{}'.".
                                 format(json_data))

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""

        videos = Video.objects.all()
        data = [{"id": o.id, "url": o.url, "description": o.description} for o in videos]
        response = json.dumps(data)

        return HttpResponse(response)

def delete_video(request, id):
    """Implements DELETE for the video API described in the README."""
    if request.method == 'DELETE':
        v = Video.objects.get(id=id)
        v.delete()
        return success()
    else:
        return HttpResponseForbidden()

