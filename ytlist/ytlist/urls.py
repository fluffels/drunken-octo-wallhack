from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django_gears.urls import gears_urlpatterns

from views import VideoAPIView
from views import IndividualVideoAPIView
from views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^videos/$', VideoAPIView.as_view()),
    url(r'^videos/(?P<id>[0-9]+)/$', IndividualVideoAPIView.as_view()),
)

if settings.DEBUG:
    urlpatterns += gears_urlpatterns()

