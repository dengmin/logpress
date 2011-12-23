#!/usr/bin/env python
# *_* encoding=utf-8*_*
from blog.blogutils import render,paginator_objects
from blog.models import *
from random import sample

def index(request):
    page = request.GET.get('page',1)
    categories = Category.objects.all()
    posts = paginator_objects(Post.objects.all(),page)
    return render(request,'wap/index.html',locals())

def post(request,id):
    post = Post.objects.get(id=id)
    return render(request,'wap/post.html',locals())

def category(request,name):
    page=request.GET.get('page',1)
    cat = Category.objects.get(slug=name)
    posts = Post.objects.get_post().filter(category=cat)
    categories = Category.objects.all()
    return render(request,'wap/archive.html',locals())

def post_type(request,type):
    number = 5
    posts = Post.objects.get_post()
    if type == 'popular':
        posts=posts.order_by('-readtimes')[:number]
    elif type== 'random':
        if number > len(posts):
            number = len(posts)
        posts=sample(posts,number)
    elif type == 'recent':
        posts = posts[:number]
    return render(request,'wap/post_type.html',locals())