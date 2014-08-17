from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from views import VideoAPIView
from views import delete_video
from views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^videos/$', VideoAPIView.as_view()),
    url(r'^videos/(?P<id>[0-9]+)/$', delete_video),
)
