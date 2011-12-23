#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from blog.mptt.models import MPTTModel
from blog.tagging.fields import TagField
from blog.tagging.models import Tag

from blog.managers import PostManager,PageManager

class Category(MPTTModel):
    name=models.CharField(max_length=50,verbose_name=u'目录名称')
    slug=models.SlugField(verbose_name=u'Slug')
    parent = models.ForeignKey('self', null=True, blank=True,
                               verbose_name='父目录',
                               related_name='children')
    desc=models.TextField(null=True, blank=True,verbose_name=u'描述')
    
    @property
    def count(self):
        return Post.objects.get_post().filter(category=self).count()
    
    def get_absolute_url(self):
        return "/category/%s"%self.slug
    
    def get_wap_url(self):
        return '/wap/cate/%s'%self.slug
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table='blog_category'
    
class Comment(MPTTModel):
    
    author   = models.CharField(max_length = 50,verbose_name=u'用户')
    email  = models.EmailField(verbose_name=u'Email地址')
    weburl   = models.URLField(verbose_name=u'站点')
    content = models.TextField(max_length=3000,verbose_name=u'内容')
    
    parent = models.ForeignKey('self', null=True, blank=True,
                               related_name = 'children')
    # Metadata about the comment
    ip_address  = models.IPAddressField( blank=True, null=True,verbose_name=u'ip地址')
    is_public   = models.BooleanField(default=True)
    date = models.DateTimeField(editable=False,verbose_name=u'发布日期')
    useragent=models.CharField(max_length=300,editable=False)
    content_type   = models.ForeignKey(ContentType,editable=False)
    object_pk      = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    def get_content_object_url(self):
        model = ContentType.objects.get(pk = self.content_type_id).model_class()
        object = model.objects.get(pk = self.object_pk)
        return object.get_absolute_url()

    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)
    
    @property
    def object(self):
        model = ContentType.objects.get(pk = self.content_type_id).model_class()
        return model.objects.get(pk = self.object_pk)
    
    def __unicode__(self):
        return self.content
    
    class Meta:
        db_table='blog_comment'
        ordering = ['-date']

class Post(models.Model):
    author=models.ForeignKey(User,verbose_name=u'文章作者')
    category= models.ForeignKey(Category,verbose_name=u'文章分类') #文章分类
    title = models.CharField(max_length=200,verbose_name=u'标题')
    content = models.TextField(verbose_name=u'内容')
    #标签
    tags=TagField(verbose_name=u'标签',help_text=u'多个标签请用英文逗号分开')
    #阅读的次数
    readtimes = models.IntegerField(default=0,editable=False,verbose_name=u'浏览次数')
    slug = models.CharField(max_length=100, null=True, blank=True,verbose_name='Slug',\
                            help_text=u'Slug可以提高 URLs 的可读性和对搜索引擎的友好程度')
    link = models.CharField(max_length=100, null=True, blank=True,editable=False)
    #允许评论
    allow_comment = models.BooleanField(default=True,verbose_name=u'这篇文章接受用户评论')
    allow_pingback = models.BooleanField(default=True,verbose_name=u'这篇文章接受pingback')
    #文章置顶
    published = models.BooleanField(default=True,verbose_name='发布这篇文章')
    sticky=models.BooleanField(default=False,verbose_name=u'置顶这篇文章到首页')
    #所有评论
    comments =  generic.GenericRelation(Comment, object_id_field='object_pk',
                                        content_type_field='content_type')
    date = models.DateTimeField(auto_now_add=True)
    
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/archive/%s.html'%(str(self.id))
    
    def get_wap_url(self):
        return '/wap/%s.html'%(str(self.id))
    @property
    def get_comments(self):
        return self.comments.filter(is_public=True)
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)
    
    def next(self):
        '''下一篇文章'''
        next = Post.objects.filter(published=True,date__gt=self.date).order_by('date')
        if len(next) >0:
            return next[0]
        else :
            return None
        
    def prev(self):
        '''上一篇文章'''
        prev = Post.objects.filter(published=True,date__lt=self.date)
        if len(prev)>0:
            return prev[0]
        else:
            return None
    
    @property
    def excerpt_content(self):
        return self.__get_excerpt_content('Read More...')
    
    def __get_excerpt_content(self,more='Read More...'):
        spl=self.content.split('<!--more-->')
        if len(spl) > 1:
            return spl[0]+u' <a class="readmore" href="/%s">%s</a>'%(self.link,more)
        else:
            return spl[0]
            
    def updateReadtimes (self):
        self.readtimes += 1
        super(Post,self).save()
    
    class Meta:
        db_table='blog_post'
        ordering = ['-sticky' ,'-date']
    
class OptionSet(models.Model):
    key=models.CharField(max_length=100)
    value=models.TextField()
    
    @classmethod
    def set(cls,k,v):
        os,created = OptionSet.objects.get_or_create(key=k)
        os.value=v
        os.save()
        return os
    
    @classmethod
    def get(cls,k,v=''):
        try:
            option=OptionSet.objects.get(key=k)
        except:
            option=OptionSet.set(k, v)
        return option.value
    
    @classmethod
    def deloption(cls,k):
        return OptionSet.objects.get(key=k).delete()
    
    class Meta:
        db_table = 'blog_optionset'

class Page(models.Model):
    author=models.ForeignKey(User,verbose_name=u'作者') #作者
    title = models.CharField(max_length=200,verbose_name=u'标题')  #页面标题
    content = models.TextField(verbose_name=u'内容')  #页面内容
    slug = models.CharField(max_length=100, null=True, blank=True,verbose_name=u'Slug')
    allow_comment = models.BooleanField(default=True,verbose_name=u'这篇文章接受用户评论')
    allow_pingback = models.BooleanField(default=True,verbose_name=u'这个文章接受pingback')
    published = models.BooleanField(default=True,verbose_name='发布这个页面')
    menu_order = models.IntegerField(default=0,verbose_name=u'页面排序')  #排序
    readtimes = models.IntegerField(default=0,editable=False,verbose_name=u'浏览次数')
    #所有评论
    comments =  generic.GenericRelation(Comment, object_id_field='object_pk',
                                        content_type_field='content_type')
    date = models.DateTimeField(auto_now_add=True)
    
    objects = PageManager()
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/page/%s.html"%self.id
    
    @property
    def get_comments(self):
        return self.comments.filter(is_public=True)
    
    def delete(self):
        '''删除之前现把该页面下的所有评论删除'''
        self.comments.all().delete()
        super(Page,self).delete()
        
    class Meta:
        db_table = 'blog_page'
        ordering = ['-date']
   
class Link(models.Model):
    '''友情链接'''
    text=models.CharField(max_length=20,verbose_name=u'名称')
    href=models.URLField(verbose_name=u'链接')
    comment=models.CharField(max_length=50,null=True, blank=True,default='',verbose_name=u'备注')
    createdate=models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        db_table = 'blog_link'

class Blog:
    
    def __init__(self):
        self.blogtitle = OptionSet.get('blogtitle', 'LogPress')
        self.subtitle = OptionSet.get('subtitle','a simple blog named logpress')
        self.sitekeywords = OptionSet.get('sitekeywords', 'blog,sae,django,python,youflog')
        self.sitedescription = OptionSet.get('sitedescription', 'a blog system')
        self.theme_name = OptionSet.get('theme_name','classic')
