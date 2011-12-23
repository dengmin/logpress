#!/usr/bin/env python
# *_* encoding=utf-8*_*
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.utils.http import http_date
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.conf import settings
from blog.models import *
from blog.tagging.models import TaggedItem
from blog.forms import CommentForm
from blog.blogutils import render,render_to_theme,paginator_objects

import re

def get_comment_cookie_meta(request):
    author = ''
    email = ''
    weburl = ''
    if 'author' in request.COOKIES:
        author = request.COOKIES['author']
    if 'email' in request.COOKIES:
        email = request.COOKIES['email']
    if 'weburl' in request.COOKIES:
        weburl = request.COOKIES['weburl']
    return {'author': author, 'email': email, 'url': weburl}

def home(request):
    page = request.GET.get('page',1)
    posts = paginator_objects(Post.objects.get_post(),page)
    ishome=True
    return render_to_theme(request,'index.html',locals())


def post(request,id):
    post = Post.objects.get(id=id)
    post.updateReadtimes()
    comment_meta = get_comment_cookie_meta(request)
    return render_to_theme(request,'single.html',locals())


def page(request,id):
    post = Page.objects.get(id=id)
    comment_meta = get_comment_cookie_meta(request)
    return render_to_theme(request,'page.html',locals())

class CommentPostBadRequest(HttpResponseBadRequest):
    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("400-debug.html", {"why": why})

def post_coment(request):
    data = request.POST.copy()
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
        
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
    except (TypeError,AttributeError,ObjectDoesNotExist):
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % \
                (escape(ctype), escape(object_pk)))

    form = CommentForm(target, data=data)
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    if form.errors:
        message = None
        for field in ['author', 'email', 'content', 'url']:
            if field in form.errors:                                              
                if form.errors[field][0]:                                         
                    message = '[%s] %s' % (field.title(), form.errors[field][0].capitalize())
                    break
        return render_to_response('400-debug.html', {'why': message})

    comment = form.get_comment_object()
    comment.ip_address = request.META.get("REMOTE_ADDR", None)
    comment.useragent=request.META.get('HTTP_USER_AGENT','unknown')
    
    reg = re.compile(u"[\u4e00-\u9fa5]")
    if reg.findall(comment.content):
        comment.is_public=True
    else:
        comment.is_public=False
    comment.save()
    response = HttpResponseRedirect(comment.get_absolute_url())
    try:
        response.set_cookie('author', comment.author, max_age = 31536000)
        response.set_cookie('email', comment.email, max_age = 31536000)
        response.set_cookie('weburl', comment.weburl, max_age = 31536000)
    except:
        pass
    return response

def archives(request,year,month):
    page=request.GET.get('page',1)
    posts=paginator_objects(Post.objects.get_post_by_year_month(year,month),page)
    archtype='archive'
    return render_to_theme(request,'archive.html',locals())

def category(request,name):
    page=request.GET.get('page',1)
    cat = Category.objects.get(slug=name)
    posts = paginator_objects(Post.objects.get_post().filter(category=cat),page)
    archtype='category'
    return render_to_theme(request,'archive.html',locals())

def tags(request,tag):
    page=request.GET.get('page',1)
    tag = get_object_or_404(Tag, name =tag)
    posts = paginator_objects(TaggedItem.objects.get_by_model(Post, tag).order_by('-date'),page)
    archtype='tag'
    return render_to_theme(request,'archive.html',locals())

def calendar(request,year,month,day):
    page=request.GET.get('page',1)
    posts=paginator_objects(Post.objects.get_post_by_day(year,month,day),page)
    archtype='calendar'
    return render_to_theme(request,'archive.html',locals()) 
    
from django.db.models import Q
from django.utils.html import escape
def search(request):
    page=request.GET.get('page',1)
    query = escape(request.GET.get('s', ''))
    qd = request.GET.copy()
    if 'page' in qd:
        qd.pop('page')
    posts=None
    if query:
        qset = (
            Q(title__icontains=query)
        )
        posts = paginator_objects(Post.objects.filter(qset, published=True).distinct(),page)
    return render_to_theme(request,'search.html',locals())