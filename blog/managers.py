#!/usr/bin/env python
# *_* encoding=utf-8*_*
#!/usr/bin/env python
# *_* encoding=utf-8*_*
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode


class PostManager(models.Manager):
    
    def get_post(self):
        return super(PostManager, self).get_query_set().filter(published=True)
    
    def get_post_by_year_month(self,year,month):
        return super(PostManager, self).get_query_set().\
            filter(published=True,
            date__year=int(year),date__month=int(month))
    
    def get_post_by_day(self,year,month,day):
        return super(PostManager, self).get_query_set().\
            filter(published=True,
            date__year=int(year),date__month=int(month),date__day=int(day))


class PageManager(models.Manager):
    
    def get_pages(self):
        return super(PageManager,self).get_query_set().filter(published=True)