#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django.contrib import admin
from django import forms
from django.db import models

from blog.models import *
from blog.forms import PageForm,PostForm
from blog.mptt.admin import MPTTModelAdmin

class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name','parent','desc','count')
    list_per_page = 20
    
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('author','title','published','category','tags','readtimes','allow_comment')
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('author','category','title', 'content', 'tags','slug')
        }),
        ('高级选项', {
            'classes': ('collapse',),
            'fields': ('password','allow_comment', 'allow_pingback','published','sticky',)
        }),
    )
    

class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ('author','title','published','slug')
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('author','title', 'content', 'slug')
        }),
        ('高级选项', {
            'classes': ('collapse',),
            'fields': ('allow_comment', 'allow_pingback','published',)
        }),
    )
    
class CommentAdmin(MPTTModelAdmin):
    list_display = ('author','email','content','is_public','ip_address','date')
    search_fields = ('author','email',)
    list_per_page = 20

class LinkAdmin(admin.ModelAdmin):
    list_display = ('text', 'href', 'comment','createdate')
    list_per_page = 20


admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Link,LinkAdmin)       