#!/usr/bin/env python
# *_* encoding=utf-8*_*

import os
from datetime import date, timedelta
from calendar import LocaleHTMLCalendar

from blog.models import Post
from django.core.urlresolvers import reverse

class LogpressCalendar(LocaleHTMLCalendar):
    
    def __init__(self):
        LocaleHTMLCalendar.__init__(self,locale='zh_CN.UTF-8')
    
    def formatday(self, day, weekday):
        if day and day in self.day_posts:
            day_date = date(self.current_year, self.current_month, day)
            archive_day_url = reverse('post_by_calendar',
                                      args=[day_date.strftime('%Y'),
                                            day_date.strftime('%m'),
                                            day_date.strftime('%d')])
            return '<td class="%s entry"><a href="%s">%d</a></td>' % (
                self.cssclasses[weekday], archive_day_url, day)
        
        return super(LogpressCalendar, self).formatday(day, weekday)
    
    def formatmonth(self, theyear, themonth, withyear=True):
        self.current_year = theyear
        self.current_month = themonth
        self.day_posts = [posts.date.day for posts in
                            Post.objects.get_post_by_year_month(theyear, themonth)]
        return super(LogpressCalendar, self).formatmonth(theyear, themonth, withyear)
    