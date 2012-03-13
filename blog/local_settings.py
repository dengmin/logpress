#!/usr/bin/env python
# *_* encoding=utf-8*_*

import os

_debug=False

BLOG_NAME = 'LogPress'
BLOG_SUB_NAME = 'a blog engine powerby django running on SAE'
BLOG_SITE_KEYWORDS='blog,sae,django,python,logpress'
BLOG_SITE_DESCRIPTION=''
#博客域名
if 'APP_NAME' in os.environ:
    BLOG_DOMAIN="http://%s"%os.environ['APP_NAME']
else:
    _debug=True
    BLOG_DOMAIN="http://127.0.0.1:8080"

#sae 文件存储的domain
STORAGE_DOMAIN='attachment'

#email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'minhao123@gmail.com'
EMAIL_HOST_PASSWORD = 'dengmin19871010'
EMAIL_PORT = 587

if _debug:
    DATABASES = {
        'default': {
            'ENGINE': 'mysql', 
            'NAME': 'blog', 
            'USER': 'root', 
            'PASSWORD': 'root',
            'HOST': '0.0.0.0', 
            'PORT': '3306',
        }
    }
else:
    import sae.core
    app = sae.core.Application()
    DATABASES = {
        'default': {
            'ENGINE': 'mysql', 
            'NAME': app.mysql_db,
            'USER': app.mysql_user, 
            'PASSWORD': app.mysql_pass,
            'HOST': app.mysql_host,
            'PORT': app.mysql_port,
        }
    }