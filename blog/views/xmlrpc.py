#! /usr/bin/env python
#coding=utf-8
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from xmlrpclib import Fault,DateTime
from django.contrib.auth.models import User
try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt
from blog.models import Post,Category
from django.conf import settings

def authenticate(username, password):
    try:
        user = User.objects.get(username__exact=username)
    except User.DoesNotExist:
        raise Fault(LOGIN_ERROR, _('Username is incorrect.'))
    if not user.check_password(password):
        raise Fault(LOGIN_ERROR, _('Password is invalid.'))
    return user

def user_structure(user):
    return {'userid':user.pk,'email':user.email,'nickname':user.username,
            'lastname': user.last_name,
            'firstname': user.first_name,
            'url':settings.BLOG_DOMAIN
            }

def post_structure(post):
    return {'title':post.title,
            'description':post.content,
            'dateCreated':DateTime(post.date),
            'categories':[cate.name for cate in Category.objects.all()],
            'link':settings.BLOG_DOMAIN+post.get_absolute_url(),
            'permalink':settings.BLOG_DOMAIN+post.get_absolute_url(),
            'postid':post.pk,
            'userid':post.author.username,
            'mt_excerpt':post.excerpt_content,
            'mt_allow_comments':post.allow_comment,
            'mt_allow_comments':post.allow_pingback,
            'mt_keywords':post.tags,
            'sticky':post.sticky,
            'wp_password':post.password,
            'wp_slug':post.slug,
            'wp_author':post.author.username,
            'wp_author_id':post.author.pk,
            'wp_author_display_name':post.author.username
            }

def category_structure(cate):
    return {'title':cate.name,'categoryId':cate.pk,'description':cate.desc,
            'htmlUrl':settings.BLOG_DOMAIN+cate.get_absolute_url(),
            'rssUrl':'','categoryName':cate.name,
            'categoryDescription':cate.desc
            }

def getUsersBlogs(appkey,username,password):
    authenticate(username,password)
    return [{'url':settings.BLOG_DOMAIN,'blogid':settings.SITE_ID,'blogName':'logpress'}]

def getUserInfo(appkey,username,password):
    user = authenticate(username,password)
    return user_structure(user)
    
def getRecentPosts(blogid,username,password,number):
    authenticate(username,password)
    return [ post_structure(post) for post in Post.objects.all()[:number]]

def newPost(blogid,username,password,post,publish):
    pass

def getPost(postid,username,password):
    authenticate(username,password)
    post = Post.objects.get(id=postid)
    return post_structure(post)
    

def editPost(postid,username,password,post,publish):
    authenticate(username,password)
    post = Post.objects.get(id=postid)

def deletePost(appkey,postid,username,password,publish):
    authenticate(username,password)
    post = Post.objects.get(id=postid)
    post.delete()
    return True

def getCategories(blogid,username,password):
    authenticate(username,password)
    return [category_structure(cate) for cate in Category.objects.all()]

def newMediaObject(blogid,username,password,file):
    authenticate(username,password)
    pass

class LogPressXMLRPCDispatcher(SimpleXMLRPCDispatcher):
    
    def __init__(self,funcs):
        SimpleXMLRPCDispatcher.__init__(self, True, 'utf-8')
        self.funcs = funcs
        
        
dispatcher = LogPressXMLRPCDispatcher({
        'blogger.getUsersBlogs': getUsersBlogs,
        'blogger.getUserInfo':getUserInfo,
        'blogger.deletePost':deletePost,
        
        'metaWeblog.getCategories':getCategories,
        'metaWeblog.getRecentPosts':getRecentPosts,
        'metaWeblog.getPost':getPost,
        'metaWeblog.newPost':newPost,
        'metaWeblog.editPost':editPost,
        'metaWeblog.newMediaObject':newMediaObject,
        
        'mt.getCategoryList':getCategories,    
        
        'wp.getUsersBlogs' :getUsersBlogs,
})

@csrf_exempt
def xmlrpc_handler(request):
    if request.method == 'POST':
        print request.raw_post_data
        return HttpResponse(dispatcher._marshaled_dispatch(request.raw_post_data))
    elif request.method == 'GET':
        response = '\n'.join(dispatcher.system_listMethods())
        return HttpResponse(response, mimetype='text/plain')