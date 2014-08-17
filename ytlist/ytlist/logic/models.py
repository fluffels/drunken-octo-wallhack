from django.db import models

class Video(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=500)

    def __str__(self):
        return "{}".format(self.url)

