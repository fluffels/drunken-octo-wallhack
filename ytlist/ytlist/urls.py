from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from ytlist.logic.views import VideoAPIView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^videos/$', VideoAPIView.as_view()),
)
