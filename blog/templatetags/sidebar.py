#!/usr/bin/env python
# *_* encoding=utf-8*_*
from django.template import Library
from datetime import date, timedelta,datetime
from random import sample

from blog.models import *

register = Library()

@register.inclusion_tag('sidebar/post.html', takes_context = True)
def get_recent_posts(context,number=5):
    posts=Post.objects.get_post()
    if number > len(posts):
        number = len(posts)
    return {'posts':posts[:number]}

@register.inclusion_tag('sidebar/post.html', takes_context = True)
def get_popular_posts(context,number=5):
    posts=Post.objects.get_post().order_by('-readtimes')
    if number > len(posts):
        number = len(posts)
    return {'posts':posts[:number]}

@register.inclusion_tag('sidebar/post.html', takes_context = True)
def get_random_posts(context,number=5):
    posts = Post.objects.get_post()
    if number > len(posts):
        number = len(posts)
    return {'posts':sample(posts,number)}

@register.inclusion_tag('sidebar/categories.html', takes_context = True)
def get_categories(context):
    return {'nodes':Category.tree.all()}

@register.inclusion_tag('sidebar/meta.html', takes_context = True)
def get_meta_widget(context):
    return {'user':context.get('request').user}

@register.inclusion_tag('sidebar/archives.html', takes_context = True)
def get_archives(context):
    return {'archives':Post.objects.dates('date','month','DESC')}

@register.inclusion_tag('sidebar/links.html', takes_context = True)
def get_links(context):
    return {'links':Link.objects.all()}

@register.inclusion_tag('sidebar/menus.html', takes_context = True)
def get_menus(context):
    current = 'current' in context and context['current']
    menus = Page.objects.get_pages()
    return {'menus':menus,'current':current}

@register.inclusion_tag('sidebar/tags.html', takes_context = True)
def get_tag_cloud(context):
    return locals()

@register.inclusion_tag('sidebar/comments.html', takes_context = True)
def get_recent_comments(context):
    comments = Comment.objects.filter(is_public=True)
    return {'comments':comments[:8]}

@register.inclusion_tag('sidebar/site_analytics.html', takes_context = True)
def get_site_analytics(context):
    return {'content':OptionSet.get('site_analytics','')}

@register.inclusion_tag('sidebar/calendar.html',takes_context=True)
def get_calendar(context,year=None, month=None):
    if not year or not month:
        if context.get('year'):
            year = int(context.get('year'))
        if context.get('month'):
            month = int(context.get('month'))
        if not year or not month:
            date_month = datetime.today()
            year, month = date_month.timetuple()[:2]
    try:
        from blog.logpresscalendar import LogpressCalendar
    except ImportError:
        return {'calendar': '<p class="notice">Calendar is unavailable for Python<2.5.</p>'}
    
    calendar = LogpressCalendar()
    
    current_month = datetime(year, month, 1)
    dates = list(Post.objects.dates('date', 'month'))
    
    if not current_month in dates:
        dates.append(current_month)
        dates.sort()
    index = dates.index(current_month)

    previous_month = index > 0 and dates[index - 1] or None
    next_month = index != len(dates) - 1 and dates[index + 1] or None
    
    return {'next_month': next_month,
            'previous_month': previous_month,
            'calendar':calendar.formatmonth(year, month)}