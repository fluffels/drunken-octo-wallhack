import json

from django.http import HttpResponse
from django.views.generic import View

class VideoAPIView(View):
    """Implements the video API described in the README."""
    http_method_names = ['get', 'post', 'delete']

    def error(self, status, message):
        """Return an error messsage formatted as a JSON object."""

        error = {"status": status, "message": message}
        return HttpResponse(json.dumps(error))

    def success(self):
        """Return a success message formatted as a JSON object."""

        success = {"status": 0, "message": ""}
        return HttpResponse(json.dumps(success))

    def post(self, request, *args, **kwargs):
        """Handle POST requests."""

        if ("data" not in request.POST):
            return self.error(1, ('Please send a valid JSON object in the '
                                  '"data" field of the POST request.'))
        else:
            json_data = request.POST["data"]

            try:
                video = json.loads(json_data)
            except Exception as e:
                return self.error(2, "Error while parsing JSON string '{}': {}".
                                      format(json_data, e))

            return self.success()

