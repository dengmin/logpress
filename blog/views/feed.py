#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sitemaps import Sitemap
from blog.models import Post,Comment
from django.conf import settings

class PostFeed(Feed):
    
    title = 'logpress'
    link = settings.BLOG_DOMAIN
    description  = 'python blog '
    
    def items(self):
        return Post.objects.get_post()[:20]
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt_content
    
    def item_pubdate(self, item):
        return item.date
    
    def item_link(self,item):
        return '%s%s'%(settings.BLOG_DOMAIN ,item.get_absolute_url())
    

class AtomPostFeed(PostFeed):
    feed_type = Atom1Feed
    subtitle = PostFeed.description

class CommentFeed(Feed):
    title = 'logpress'
    description  = 'python blog '
    link = settings.BLOG_DOMAIN
    
    def items(self):
        return Comment.objects.filter(is_public=True)[:10]

    def item_title(self, item):
        return item.author
    
    def item_pubdate(self, item):
        return item.date

    def item_description(self, item):
        return item.content
    
    def item_link(self,item):
        return '%s%s'%(settings.BLOG_DOMAIN ,item.get_absolute_url())
    

class BlogSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    def items(self):
        return Post.objects.get_post()

    def lastmod(self, item):
        return item.date
    
    def location(self,item):
        return item.get_absolute_url()
    
    def __get(self, name, obj, default=None):
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr
    
    def get_urls(self, page=1, site=None):
        urls = []
        for item in self.paginator.page(page).object_list:
            loc = "%s%s" % (settings.BLOG_DOMAIN, self.__get('location', item))
            priority = self.__get('priority', item, None)
            url_info = {
                'location':   loc,
                'lastmod':    self.__get('lastmod', item, None),
                'changefreq': self.__get('changefreq', item, None),
                'priority':   str(priority is not None and priority or '')
            }
            urls.append(url_info)
        return urls