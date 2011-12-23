#!/usr/bin/env python
# *_* encoding=utf-8*_*

from blog.models import Blog
from django.conf import settings

def context(request):
    blog = Blog()
    return {
            'blog':blog,
            'request':request,
            'settings':settings
            }