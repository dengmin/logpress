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
from blog.forms import PostForm,PageForm

from django.conf import settings

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt
from blog.weibo import weibo_client

def settings(request):
    binded = OptionSet.get('bind_weibo','')=='True'
    return render(request,'admin/settings.html',locals())

def _get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/'
    return referer_url

@login_required
def bind_sina_weibo(request):
    back_to_url = _get_referer_url(request)
    request.session['login_back_to_url'] = back_to_url
    login_backurl = request.build_absolute_uri('/weibo/bind_callback/')
    auth_url = weibo_client.get_authorization_url_with_callback(login_backurl)
    request.session['oauth_request_token'] = weibo_client.request_token
    return HttpResponseRedirect(auth_url)

@login_required
def bind_callback(request):
    verifier = request.GET.get('oauth_verifier', None)
    request_token = request.session['oauth_request_token']
    del request.session['oauth_request_token']
    weibo_client.set_request_token(request_token.key, request_token.secret)
    access_token = weibo_client.get_access_token(verifier)
    
    request.session['oauth_access_token'] = access_token
    
    back_to_url = request.session.get('login_back_to_url', '/')
    OptionSet.set('bind_weibo','True')
    OptionSet.set('weibo_access_token_key',access_token.key)
    OptionSet.set('weibo_access_token_secret',access_token.secret)
    return HttpResponseRedirect(back_to_url)

@login_required
def unbind_weibo(request):
    back_to_url = _get_referer_url(request)
    OptionSet.set('bind_weibo','False')
    OptionSet.set('weibo_access_token_key','')
    OptionSet.set('weibo_access_token_secret','')
    return HttpResponseRedirect(back_to_url)