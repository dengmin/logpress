#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from blog.blogutils import render
from blog.models import *
from blog.forms import PostForm,CategoryForm,PageForm

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt
