#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django.dispatch import Signal
from blog.blogutils import sendmail
from blog.models import OptionSet
from django.conf import settings

comment_was_submit=Signal(providing_args=['comment'])

def on_comment_was_submit(sender,comment,*args,**kwargs):
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


comment_was_submit.connect(on_comment_was_submit)