import requests

from xml.dom import minidom

from django.db import models

class Video(models.Model):
    url = models.URLField()
    description = models.TextField()
    title = models.TextField()

    def __str__(self):
        return "{}".format(self.url)

    def fetch_details(self):
        g_api_url = "https://gdata.youtube.com/feeds/api/videos/{}?v=2".format(self.url)
        response = requests.get(g_api_url)

        xml = minidom.parseString(response.content)

        try:
            self.title = xml.getElementsByTagName("media:title")[0].firstChild.wholeText
            self.description = xml.getElementsByTagName("media:description")[0].firstChild.wholeText
        except:
            self.title = "No title."
            self.description = "No description."

        self.save()

