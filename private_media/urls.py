from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('private_media.views',
    url(r'^{0}(?P<path>.*)$'.format(settings.PRIVATE_MEDIA_URL.lstrip('/')), 'serve_private_file',),
)
