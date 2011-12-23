#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django.contrib import admin
from django import forms
from django.db import models

from blog.models import *

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'id':'content','cols':90,'rows':20})
    class Media:
        js= (
             '/static/kindeditor/kindeditor-min.js',
             '/static/kindeditor/lang/zh_CN.js',
             '/static/kindeditor/textarea.js',
             )
    class Meata:
        model = Post

class PageForm(PostForm):
    class Meata:
        model = Page

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent','desc','count')
    
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('author','title','published','category','tags','readtimes','allow_comment')
    fieldsets = (
        (None, {
            'fields': ('author','category','title', 'content', 'tags','slug')
        }),
        ('高级选项', {
            'classes': ('collapse',),
            'fields': ('allow_comment', 'allow_pingback','published','sticky',)
        }),
    )
    

class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ('author','title','published','slug')
    fieldsets = (
        (None, {
            'fields': ('author','title', 'content', 'slug')
        }),
        ('高级选项', {
            'classes': ('collapse',),
            'fields': ('allow_comment', 'allow_pingback','published',)
        }),
    )
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','email','content','is_public','ip_address','date')
    search_fields = ('author','email',)

class LinkAdmin(admin.ModelAdmin):
    list_display = ('text', 'href', 'comment','createdate')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Link,LinkAdmin)       