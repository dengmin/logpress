#!/usr/bin/env python
# *_* encoding=utf-8*_*
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^themes/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_DIR+'/templates/themes/',}),
    (r'^admin/', include(admin.site.urls)),
    (r'',include('blog.views.urls')),
)
