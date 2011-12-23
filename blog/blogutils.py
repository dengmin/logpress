#!/usr/bin/env python
# *_* encoding=utf-8*_*
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def render(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)

def render_to_theme(request,theme_file,template_ctx):
    theme = 'classic'
    tpl_file='themes/'+theme+'/'+theme_file
    return render(request,tpl_file,template_ctx)


def paginator_objects(objs, page,pagesize=10):
    '''分页'''
    paginator = Paginator(objs, pagesize)
    try:
        ret = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ret = paginator.page(paginator.num_pages)

    return ret