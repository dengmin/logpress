#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django.conf import settings
from blog.blogutils import theme

def context(request):
    return {
            'request':request,
            'settings':settings,
            'theme':theme
            }