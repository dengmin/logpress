#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django.dispatch import Signal
from blog.blogutils import sendmail
from blog.weibo import weibo_client
from django.conf import settings

post_was_submit = Signal(providing_args=['post'])

comment_was_submit=Signal(providing_args=['comment'])

def on_post_was_submit(sender,post,*args,**kwargs):
    try:
        from blog.models import OptionSet
        bind = OptionSet.get('bind_weibo','')=='True'
        if bind:
            access_token_key = OptionSet.get('weibo_access_token_key','')
            access_token_secret = OptionSet.get('weibo_access_token_secret','')
            weibo_client.setToken(access_token_key,access_token_secret)
            from weibopy.api import API
            api = API(weibo_client)
            api.update_status(status='[%s] %s ... %s'\
                              %(post.title,post.content[:60],settings.BLOG_DOMAIN+post.get_absolute_url()))
    except:
        pass
     

def on_comment_was_submit(sender,comment,*args,**kwargs):
    from blog.models import OptionSet
    if comment.parent:
        parent = comment.parent
        if parent.email and parent.is_public == True:
            blogtitle = OptionSet.get('blogtitle', 'LogPress')
            subject=u'您在 [ %s ] 上的评论有了新的回复!!!'%(blogtitle)
            sendmail('email/reply_comment.txt',{'comment':comment,\
                                                'settings':settings,\
                                                'blogtitle':blogtitle}\
                                        ,subject,parent.email)
    else:
        if comment.email and comment.is_public==True:
            subject=u'文章[%s]有了新的评论了!!!'%(comment.object)
            sendmail('email/new_comment.txt',{'comment':comment,'settings':settings},subject,comment.email)

post_was_submit.connect(on_post_was_submit)
comment_was_submit.connect(on_comment_was_submit)