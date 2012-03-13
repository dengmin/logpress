#!/usr/bin/env python
# *_* encoding=utf-8*_*
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.template.context import Context
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

theme = False

def render(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)

def render_to_theme(request,theme_file,template_ctx):
    global theme
    if not theme:
        from blog.models import OptionSet
        theme = OptionSet.get('blog_theme','classic')
    tpl_file='themes/%s/%s' % (theme , theme_file)
    return render(request,tpl_file,template_ctx)


def paginator_objects(objs, page,pagesize=10):
    '''分页'''
    paginator = Paginator(objs, pagesize)
    try:
        ret = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ret = paginator.page(paginator.num_pages)
    return ret

def sendmail(template,template_data,subject,reveivers):
    template = get_template(template)
    msg = template.render(Context(template_data))
    try:
        from sae.mail import EmailMessage
        m = EmailMessage()
        m.to = reveivers
        m.subject = subject
        m.html = msg
        m.smtp = (settings.EMAIL_HOST, settings.EMAIL_PORT, \
                  settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.EMAIL_USE_TLS)
        m.send()
    except ImportError:
        pass
