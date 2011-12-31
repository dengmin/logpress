#!/usr/bin/env python
# *_* encoding=utf-8*_*
from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as sitemap_views
from django.conf import settings

from blog.views import index,wap,admin
from blog.views.feed import PostFeed,AtomPostFeed,CommentFeed,BlogSiteMap

sitemaps = {
    'posts': BlogSiteMap(),
}

CACHE_TIME = 60*60*6 

urlpatterns = patterns('',
    url(r'^$',index.home,name='index_home'),
    url(r'^archive/(?P<id>\d+).html',index.protect_post(index.post),name="post"),
    url(r'^post/password/(?P<id>\d+)',index.post_password,name='post_by_password'),
    url(r'^page/(?P<id>\d+)',index.page,name="page"),
    url(r'comment/post',index.post_coment,name='post_comment'),
    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})$', index.archives,name='retrieve_post__by_month'),
    url(r'^category/(?P<name>[-\w]+)$',index.category,name='retrieve_post_by_category'),
    url(r'^tag/(?P<tag>[-\w]+)/$', index.tags, name='retrieve_post_by_tag'),
    url(r'^calendar/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})',index.calendar,name='post_by_calendar'),
    url(r'^search$',index.search,name='search'),
    
    #feed
    url(r'^feed/post$',cache_page(PostFeed(),CACHE_TIME),name="feed_post"),
    url(r'^atom$',cache_page(AtomPostFeed(),CACHE_TIME),name="atom"),
    url(r'^feed/comment$',cache_page(CommentFeed(),60*60*6),name="feed_comment"),
    #sitemap
    url(r'^sitemap.xml$', cache_page(sitemap_views.sitemap, CACHE_TIME),{'sitemaps': sitemaps},name='sitemap'),
)


urlpatterns += patterns('',
    url(r'^wap$',wap.index,name='wap_index'),
    url(r'^wap/(?P<id>\d+)',wap.post,name="wap_post"),
    url(r'^wap/cate/(?P<name>[-\w]+)',wap.category,name='wap_post_category'),
    url(r'^wap/post/(?P<type>[-\w]+)',wap.post_type ,name='wap_post_type'),
)

urlpatterns += patterns('',
     url(r'^admin/file_manager_json',admin.file_manager_json,name='file_manager_json'),
     url(r'^admin/file_upload_json',admin.file_upload_json,name='file_upload_json'),
     url(r'^admin/settings',admin.blog_settings,name='settings'),
     url(r'^weibo/bind$',admin.bind_sina_weibo,name='bind_weibo'),
     url(r'^weibo/bind_callback/$', admin.bind_callback, name='bind_callback'),
     url(r'^weibo/unbind$',admin.unbind_weibo,name='unbind_weibo'),          
)